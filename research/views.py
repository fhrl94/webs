import datetime

import os
import time
import zipfile

import sys

import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from django.utils.http import urlquote

from research.forms import *
from research.models import InformationEmployees

section_list = ['section_one', 'section_two', 'section_three', 'section_four', 'section_five', 'section_six', ]
form_customer = [CustomerOneForm, CustomerTwoForm, CustomerThreeForm, CustomerFourForm, CustomerFiveForm,
                 CustomerSixForm]
form_sell = [SellOneForm, SellTwoForm, SellThreeForm, SellFourForm]

@login_required(login_url="login")
def index_view(request):
    # return render(request=request, template_name='research/user_form.html')
    user = getattr(request, 'user', None)
    # print(user.id)
    # print(user)
    # print(InformationEmployees.objects.filter(emp_user = user.id))
    # 获取当前登录用户信息
    try:
        user_emp = InformationEmployees.objects.filter(emp_user=user.id).get()
    except:
        return error_404(request, "用户关联错误，请联系管理员")
    # 根据用户信息（部门、当前阶段）确定相应 表单
    auto_calculate(user_emp.pk)
    user_emp = InformationEmployees.objects.filter(emp_user=user.id).get()
    if user_emp.department == "y" and user_emp.next_section[0] == "y":
        form = form_customer[int(user_emp.next_section[1]) - 1]
    elif user_emp.department == "k" and user_emp.next_section[0] == "k":
        form = form_sell[int(user_emp.next_section[1]) - 1]
    elif user_emp.next_section == 'completed':
        return error_404(request, "已完成所有的调查")
    #  当前无问卷调查 在Form中实现了
    else:
        return error_404(request, "部门信息错误，请联系管理员")
    if request.method == 'POST':
        user_form = form(request.POST)
        if user_form.is_valid():
            #  数据写入
            new_form = user_form.save(commit=False)
            new_form.department = user_emp.department
            new_form.group = user_emp.group
            # 新增【直接上级】、【当前阶段】、【入职天数】、【联系方式】、【填表日期】
            new_form.superior_name = user_emp.superior_name
            new_form.current_section = user_emp.next_section
            new_form.enter_days = user_emp.enter_days
            new_form.tel = user_emp.tel
            new_form.enter_date = datetime.date.today()
            new_form.employees = user_emp
            new_form.score_sum = 0
            for one in user_form.fields:
                # print(one)
                if one != 'question_summary':
                    new_form.score_sum += int(user_form.cleaned_data[one])
            new_form.save()
            print(section_list[int(user_emp.next_section[1]) - 1])
            print(getattr(user_emp, section_list[int(user_emp.next_section[1]) - 1]))
            setattr(user_emp, section_list[int(user_emp.next_section[1]) - 1], True)
            user_emp.save()
            # 保存完毕后进行计算
            auto_calculate(user_emp.pk)
            return HttpResponseRedirect(reverse(home_form))
    else:  # 当正常访问时
        # user_form = CustomerOneForm()
        user_form = form()
    return render(request=request, template_name='research/form.html',
                  context={'user_form': user_form, 'user_emp': user_emp, 'today': datetime.date.today(),
                           'num': int(user_emp.next_section[1])})
    pass


# TODO 开发注册
# def web_register(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         if user_form.is_valid():
#             username = user_form.cleaned_data['user_name']
#             password = user_form.cleaned_data['password']
#             email = user_form.cleaned_data['email']
#             emp = InformationEmployees.objects.create(username=username,password=password,email=email)
#             emp.save()
#             return HttpResponse('register success!!!')
#     else:
#         user_form = UserForm()
#     return render('login.html',{'user_form':user_form})

@login_required(login_url="login")
def home_form(request):
    user = getattr(request, 'user', None)
    try:
        user_emp = InformationEmployees.objects.filter(emp_user=user.id).get()
    except:
        return error_404(request, "用户关联错误，请联系管理员")
    auto_calculate(user_emp.pk)
    user_emp = InformationEmployees.objects.filter(emp_user=user.id).get()
    research_exist = False
    body = '当前的无调查问卷'
    num = None
    if user_emp.next_section == "completed":
        body = '您已完成所有问卷'
    # 理论期数会比实际大一轮，
    elif user_emp.next_section <= user_emp.consult_section:
        # print("当前填写第{num}期".format(num=int(user_emp.next_section[1])))
        research_exist = True
        num = int(user_emp.next_section[1])
    return render(request, template_name='research/home.html',
                  context={'research_exist': research_exist, 'num': num, 'body': body})


def user_login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['账号'], password=cd['密码'])
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponseRedirect(redirect_to='/index/')
                    # return HttpResponseRedirect(request.POST.get('next', '/') or '/')
                    return HttpResponseRedirect(reverse(home_form))
                else:
                    return error_404(request, '禁止访问')
            else:
                return error_404(request, '账号或密码错误')
    else:
        form = UserForm()
    return render(request, template_name='research/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return render(request, template_name='research/logout.html')
    pass


def error_404(request, error_body):
    return render(request, template_name='research/404.html', context={'error_body': error_body, })
    pass


# TODO 实现装饰器
def auto_calculate(ID):
    """
    计算 【入职天数】、【当前阶段】、【理论阶段】
    :param ID:
    :return:
    """
    customer = {'161': 'y6', '133': 'y5', '105': 'y4', '77': 'y3', '49': 'y2', '28': 'y1', '-1': 'y0', }
    sell = {'90': 'k4', '60': 'k3', '30': 'k2', '14': 'k1', '-1': 'k0', }
    if ID is None:
        result = InformationEmployees.objects.all()
    else:
        result = InformationEmployees.objects.filter(pk=ID).all()
    for one in result:
        # print(one.enter_date)
        # print(type(one.enter_date))
        # print(type(datetime.date.today()))
        # print(type((datetime.date.today() - one.enter_date).days))
        one.enter_days = str((datetime.date.today() - one.enter_date).days)
        if one.department == "y":
            category = customer
        elif one.department == "k":
            category = sell
        else:
            raise UserWarning("部门没有维护或异常")
        # 计算理论阶段
        for section in category.keys():
            if int(section) < int(one.enter_days):
                one.consult_section = category[section]
                break  # print(one.consult_section)
        # 计算当前阶段
        for j, consult in enumerate(section_list):
            # j 从 0 开始 需要加 1
            # print(getattr(user_emp, one))
            if not getattr(one, consult):
                # 部门为客发超过4期，即完成
                if one.department == "k" and j + 1 > 4:
                    one.next_section = "completed"
                    break
                # 部门为客发，且未完成到第3期 or
                # 部门为运值，且未全部完成（共6期）
                # print(one.department + str(j+1))
                one.next_section = one.department + str(j + 1)
                break
            # 6阶段均完成，即运值已全部完成
            elif j + 1 > 6:
                one.next_section = "completed"
                break
        if one.next_section != "completed" and one.consult_section[1] >= one.next_section[1]:
            one.status = True
        else:
            one.status = False
        one.save()
    # print(type(result))
    pass

@login_required(login_url="login")
def temp_form(request, user_form, user_emp, j):
    return render(request=request, template_name='research/form_dump.html',
                  context={'user_form': user_form,
                           'user_emp': user_emp, 'num': j + 1})

@login_required(login_url="login")
def form_print(request, queryset):
    """
    获取所选取人员的已填表单,
    :param request:
    :param queryset:
    :return:
    """
    # 生存临时目录,并删除历史文件
    clear_temp()
    temp_path = sys.path[0] + '/research/temp/'
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    table_customer = [CustomerOne, CustomerTwo, CustomerThree, CustomerFour, CustomerFive, CustomerSix]
    table_sell = [SellOne, SellTwo, SellThree, SellFour]
    # table_customer = ['CustomerOne', 'CustomerTwo', 'CustomerThree', 'CustomerFour', 'CustomerFive', 'CustomerSix']
    # table_sell = ['SellOne', 'SellTwo', 'SellThree', 'SellFour']
    zip_name_list = []
    for one in queryset:
        # print(type(one))
        # print(one.__dict__)
        file_name_list = []
        if one.department == "y":
            forms = form_customer
            tables = table_customer
        elif one.department == "k":
            forms = form_sell
            tables = table_sell
        else:
            forms = None
            tables = None
            return error_404(request,"部门错误")
        for j, table in enumerate(tables):
            # print(type(one))
            # print(one.__dict__)
            # print(table)
            # if table.objects.filter(employees=one).one_none()
            if not table.objects.filter(employees=one).exists():
                break
            question = table.objects.get(employees=one.pk)
            print((question))
            user_form = forms[j](instance=question)
            html =temp_form(request, user_form, question, j).getvalue().decode('utf-8')
            # html = html.replace(r'//maxcdn', r'https://cdn')
            html = re.sub(r'<link href=.+ rel="stylesheet">',
                          r'<link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">',
                          html)
            # TODO 后期分类
            html_name = temp_path + '{emp_name}第{num}期问卷-主管{superior_name}.html'.format(
                emp_name=one.name, num=j + 1, superior_name=question.superior_name
            )
            with open(file=html_name, mode='w', encoding='utf-8') as f:
                f.write(html)
            file_name_list.append(html_name)
        # zip(file_name_list, one.superior_name)
        zip_name = '{zip_name}-共{num}份.zip'.format(
        zip_name=one.superior_name,num=len(file_name_list))
        zip(file_name_list, zip_name, path='/research/zip/')
        zip_name_list.append(sys.path[0] + '/research/zip/' + zip_name)
    result_name = "新人培养调查表单-主管{num}-{now}.zip".format(
        num=len(zip_name_list), now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    )
    zip(zip_name_list, result_name, path='/research/result/')
    return download_file(sys.path[0] + '/research/result/' + result_name, '新人培养调查问卷原始表', 'zip')
    pass

def zip(file_names, zip_name, path):
    """
    根据 file_names 打包文件
    :param file_names:
    :param zip_name:
    :return:
    """
    zip_path = sys.path[0] + path
    if not os.path.exists(zip_path):
        os.mkdir(zip_path)
    with zipfile.ZipFile(zip_path + zip_name, 'w', zipfile.ZIP_DEFLATED) as f:
        for file in file_names:
            f.write(file, os.path.basename(file))

    pass

def clear_temp():
    """
    清除上次生产的文件
    :return:
    """
    temp_dir_list = ['/research/zip/', '/research/temp/', '/research/result/']
    for one in temp_dir_list:
        if not os.path.exists(sys.path[0] + one):
            os.mkdir(sys.path[0] + one)
        for del_file in os.listdir(sys.path[0] + one):
            os.remove(sys.path[0] + one + del_file)
    pass

def file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def download_file(file_path_name, download_file_name, category):
    response = StreamingHttpResponse(file_iterator(file_path_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{name}{now}.{category}"'.format(
        name=urlquote(download_file_name),
        now=(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))),
        category=category)
    return response