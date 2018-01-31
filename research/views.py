import datetime

import os
import time
import zipfile

import sys

import re

import xlsxwriter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from django.utils.http import urlquote

from research.forms import *
from research.models import InformationEmployees
from webs import settings

section_list = ['section_one', 'section_two', 'section_three', 'section_four', 'section_five', 'section_six', ]
form_customer = [CustomerOneForm, CustomerTwoForm, CustomerThreeForm, CustomerFourForm, CustomerFiveForm,
                 CustomerSixForm]
form_sell = [SellOneForm, SellTwoForm, SellThreeForm, SellFourForm]
table_customer = [CustomerOne, CustomerTwo, CustomerThree, CustomerFour, CustomerFive, CustomerSix]
table_sell = [SellOne, SellTwo, SellThree, SellFour]


@login_required(login_url="login")
def index_view(request):
    """
    表单填写页面
    :param request:
    :return:
    """
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
    # 验证当前是否存在【未填写】的表单
    if user_emp.status is not True:
        return error_404(request, "当前没有调查问卷需要填写")
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
                    if user_form.cleaned_data[one] == "":
                        continue
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
    """
    登录后直接跳转页面， 【首页】，提示员工是否有相关问卷需要填写
    :param request:
    :return:
    """
    user = getattr(request, 'user', None)
    try:
        user_emp = InformationEmployees.objects.filter(emp_user=user.id).get()
    except:
        return error_404(request, "用户关联错误，请联系管理员")
    auto_calculate(user_emp.pk)
    user_emp = InformationEmployees.objects.filter(emp_user=user.id).get()
    if user_emp.pwd_status != True:
        return change_pwd(request)
    # 使用 js 来处理
    return render(request, template_name='research/home.html', context={'user_emp': user_emp, })


@login_required(login_url="login")
def change_pwd(request):
    login_user = getattr(request, 'user', None)
    try:
        user_emp = InformationEmployees.objects.filter(emp_user=login_user.id).get()
    except:
        return error_404(request, "用户关联错误，请联系管理员")
    if request.method == 'POST':
        form = ChangePwdForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            cd = form.cleaned_data
            # print(cd)
            user = authenticate(username=request.user.username, password=cd['old_pwd'])
            print(user)
            if user is not None:
                if user.is_active:
                    user.set_password(cd['new_pwd1'])
                    user.save()
                    user_emp.pwd_status = True
                    user_emp.save()
                    return error_404(request, '密码已修改，请重新登录')
                else:
                    return error_404(request, '禁止访问')
            else:
                return error_404(request, '原始密码错误')
        else:
            return render(request, template_name='research/change_pwd.html',
                          context={'form': form, 'error': "2次密码不一致"})
    else:
        form = ChangePwdForm()
    if user_emp.pwd_status != True:
        error_str = "首次登录，请修改密码"
    else:
        error_str = None
    return render(request, template_name='research/change_pwd.html', context={'form': form, 'error': error_str,})
    pass


def user_login(request):
    """
    用户登录，登录成功后返回 home_form(request)
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['user'], password=cd['pwd'])
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
    """
    登出
    :param request:
    :return:
    """
    logout(request)
    return render(request, template_name='research/logout.html')
    pass


def error_404(request, error_body):
    """
    异常
    :param request:
    :param error_body: 异常原因（文本)
    :return:
    """
    return render(request, template_name='research/404.html', context={'error_body': error_body, })
    pass


# TODO 实现装饰器
def auto_calculate(list_id):
    """
    计算 【入职天数】、【下一阶段阶段】、【理论阶段】
    :param list_id:
    :return:
    """
    customer = {'161': 'y6', '133': 'y5', '105': 'y4', '77': 'y3', '49': 'y2', '28': 'y1', '-1': 'y0', }
    sell = {'90': 'k4', '60': 'k3', '30': 'k2', '14': 'k1', '-1': 'k0', }
    if list_id is None:
        result = InformationEmployees.objects.all()
    else:
        result = InformationEmployees.objects.filter(pk=list_id).all()
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
        # 计算下个阶段
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
            elif j + 1 >= 6:
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
def temp_form(request, user_form, user_emp, j, one):
    """
    根据参数， 返回表单
    :param request:
    :param user_form: forms 中的 class
    :param user_emp: model 中的 class
    :param j: 期数
    :param one: 填表人
    :return:
    """
    return render(request=request, template_name='research/form_dump.html',
                  context={'user_form': user_form, 'user_emp': user_emp, 'num': j + 1, 'one': one})


@login_required(login_url="login")
def form_print(request, queryset):
    """
    根据【列表】，将已填写的表单存储、打包，下载。 实现功能
    2. 填写的问卷能在线导出（美观）， 同时按列方式打包
    * 【新人培养调查问卷原始表】
        * 【部门-直接上级-人数】
            * 【员工-直接上级-分数】
                * 【员工表单-期数】
    :param request:
    :param queryset: 选择的人员列表
    :return:
    """
    # 生存临时目录,并删除历史文件
    clear_temp()
    # table_customer = ['CustomerOne', 'CustomerTwo', 'CustomerThree', 'CustomerFour', 'CustomerFive', 'CustomerSix']
    # table_sell = ['SellOne', 'SellTwo', 'SellThree', 'SellFour']
    zip_name_dict = {}
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
            return error_404(request, "部门错误")
        for j, table in enumerate(tables):
            # print(type(one))
            # print(one.__dict__)
            # print(table)
            # if table.objects.filter(employees=one).one_none()
            if not table.objects.filter(employees_id=one.pk).exists():
                # 不存在跳过，
                continue
            # 此处使用 filter ，返回 QuerySet
            # 使用 get 返回 model 类型， forms 需要 model 类型
            # print(type(table.objects.get(employees=one.pk)), type(table.objects.filter(employees=one)))
            question = table.objects.get(employees_id=one.pk)
            # print((question))
            user_form = forms[j](instance=question)
            html = temp_form(request, user_form, question, j, one).getvalue().decode('utf-8')
            # html = html.replace(r'//maxcdn', r'https://cdn')
            html = re.sub(r'<link href=.+ rel="stylesheet">',
                          r'<link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">',
                          html)
            #  生成 HTML 文件
            html_name = '{emp_name}-第{num}期问卷-组别{group}-主管{superior_name}.html'.format(emp_name=one.name, num=j + 1,
                                                                                       group=question.group,
                                                                                       superior_name=question.superior_name)
            html_name = reg_exp(html_name)
            with open(file=sys.path[0] + '/research/temp/' + html_name, mode='w', encoding='utf-8') as f:
                f.write(html)
            file_name_list.append(sys.path[0] + '/research/temp/' + html_name)
        #  生成分类字典 zip_name_dict
        reg_zip_superior = r'组别(.*?)-主管(.*?).html'
        for file_name in file_name_list:
            re_result_temp = re.search(reg_zip_superior, file_name)
            superior = re_result_temp.group(1) + "-" + re_result_temp.group(2)
            if not zip_name_dict.get(superior, False):
                zip_name_dict[superior] = []
            zip_name_dict[superior].append(file_name)
    reg_result = r'(^.*?)-(.*?$)'
    download_list = []
    #  分类，将所有生成的 HTML 文件按照表单中填写的【直接上级】 进行汇总。可能出现兼职情况
    for key, value in zip_name_dict.items():
        temp_result = re.search(reg_result, key)
        result_name = '{group}-{superior_name}-{num}份.zip'.format(group=temp_result.group(2),
                                                                  superior_name=temp_result.group(1), num=len(value))
        zip_pack(value, result_name, path='/research/result/')
        download_list.append(sys.path[0] + '/research/result/' + result_name)
    #   下载的文件生成
    download_name = "新员工培养调查表-主管{num}人-{now}.zip".format(num=len(zip_name_dict),
                                                         now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    zip_pack(download_list, download_name, path='/research/download/', )
    return download_file(sys.path[0] + '/research/download/' + download_name, '新人培养调查问卷原始表', 'zip')
    pass


def reg_exp(re_string):
    """
    生成文件时，不能包含特殊符号
    替换 /|\:*?"<> 为_
    :param re_string:
    :return:
    """
    special_string = r'/|\:*?"<>'
    return re.sub(special_string, '_', re_string)
    pass


def zip_pack(file_names, zip_name, path):
    """
    根据 file_names 打包文件列表 ，在当前路径 + path 生成 zip 文件（zip_name）
    :param file_names: 文件路径列表
    :param zip_name:  zip文件名称
    :param path: 文件路径
    :return:
    """
    zip_path = sys.path[0] + path
    if not os.path.exists(zip_path):
        os.mkdir(zip_path)
    with zipfile.ZipFile(zip_path + zip_name, 'w', zipfile.ZIP_DEFLATED) as f:
        for file in file_names:
            # print(file)
            if os.path.exists(file):
                f.write(file, os.path.basename(file))

    pass


def clear_temp():
    """
    清除上次生产的文件
    :return:
    """
    temp_dir_list = ['/research/zip/', '/research/temp/', '/research/result/', '/research/download/',
                     '/research/excel/']
    for one in temp_dir_list:
        if not os.path.exists(sys.path[0] + one):
            os.mkdir(sys.path[0] + one)
        for del_file in os.listdir(sys.path[0] + one):
            os.remove(sys.path[0] + one + del_file)
    pass


def file_iterator(file_name, chunk_size=512):
    """
    文件下载【迭代器】 ，节省下载的内存
    :param file_name: 文件名称
    :param chunk_size:
    :return:
    """
    with open(file_name, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def download_file(file_path_name, download_file_name, category):
    """
    减少下载时，大文件的内存使用
    :param file_path_name: 文件绝对路径
    :param download_file_name: 下载的文件名称
    :param category: 下载的类型
    :return:
    """
    response = StreamingHttpResponse(file_iterator(file_path_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{name}{now}.{category}"'.format(
        name=urlquote(download_file_name), now=(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))),
        category=category)
    return response


@login_required(login_url="login")
def excel_download(request, queryset):
    """
    表格分2类下载
    3. 填写的数据能汇总，导出 excel 表
    :param request:
    :param queryset: 选择的人员列表
    :return:
    """
    clear_temp()
    result_dict = {}
    for one in queryset:
        if one.department == "y":
            tables = table_customer
        elif one.department == "k":
            tables = table_sell
        else:
            tables = None
            return error_404(request, "部门错误")
        emp_research_list = []
        # excel为空，跳过
        for num, table in enumerate(tables):
            if not table.objects.filter(employees_id=one.pk).exists():
                # print(table.length_field)
                #  选项长度，跳过的格数
                emp_research_list += [{"len": table.length_field}]
                continue
            question = table.objects.filter(employees_id=one.pk)
            # print(question.values())
            emp_research_list += question.values()  # for key, value in question.iterator():  #     print(key, value)  # print(question.values_list())
        if not result_dict.get(one.department, False):
            result_dict[one.department] = {}
        # print(emp_research_list)
        if len(emp_research_list) != 0:
            result_dict[one.department][
                one.name] = emp_research_list  # excel_write('新员工培养调查.xlsx', '/research/excel/', emp_research_list, one.department,)
    # print(result_dict)
    name = '新员工培养调查.xlsx'
    excel_write('新员工培养调查.xlsx', '/research/excel/', result_dict, )
    return download_file(sys.path[0] + '/research/excel/' + name, '新员工培养调查', 'xlsx')
    pass


def excel_write(excel_name, path, result_dict_list, ):
    """
    将 result_dict_list 按规则写入到 excel 中
    表头 自定义生成
    :param excel_name: 生成的文件名称
    :param path: 生成文件的路径
    :param result_dict_list: 要写入的字典
    --部门字典
        --人员信息汇总字典
            --个人信息列表
    :return:
    """
    # superior_name 需要体现出来
    except_field = ['id', 'department',  # 'group', # 'superior_name',
                    'current_section', 'enter_days', 'tel', 'enter_date', 'employees_id', ]
    department_dict = {'k': '客发汇总表', 'y': '运值汇总表'}
    workbook = xlsxwriter.Workbook(sys.path[0] + path + excel_name)
    normal_format = workbook.add_format(
        {'valign': 'vcenter', 'align': 'center',  # https://xlsxwriter.readthedocs.io/format.html
         'top': 1,  # 上边框，后面参数是线条宽度
         'left': 1,  # 左边框
         'right': 1,  # 右边框
         'bottom': 1  # 底边框
         })
    for group_key, group_value in result_dict_list.items():
        worksheet = workbook.get_worksheet_by_name(department_dict[group_key])
        if worksheet is None:
            # sheet生成
            worksheet = workbook.add_worksheet(department_dict[group_key])
            # worksheet.set_row(1, height='22.75', )
            # worksheet.default_row_height = 22.75
            # 设置默认行高
            worksheet.set_default_row(22.75)
            # 表头绘制
            temp_num = 1
            worksheet.write(1, temp_num - 1, "序号", normal_format)
            worksheet.write(1, temp_num, "姓名", normal_format)
            if group_key == 'k':
                table_select = table_sell
            elif group_key == 'y':
                table_select = table_customer
            else:
                raise UserWarning('无部门')
            for j, one in enumerate(table_select):
                # print(one.length_field)
                for i in range(one.length_field):
                    worksheet.write(1, temp_num + i + 1, "问题{num}".format(num=i + 1), normal_format)
                temp_num += one.length_field
                worksheet.write(1, temp_num + 1, "总分", normal_format)
                worksheet.write(1, temp_num + 2, "评价总结", normal_format)
                worksheet.write(1, temp_num + 3, "组别", normal_format)
                worksheet.write(1, temp_num + 4, "主管", normal_format)
                temp_num += 4
                print(temp_num)
                worksheet.merge_range(0, temp_num - one.length_field - 3, 0, temp_num, "第{num}问卷调查".format(num=j + 1),
                                      normal_format)  # worksheet.merge_range('B3:D4', 'Merged Cells', normal_format)
        row = 2
        print(group_value)
        # 运值表、客发表
        for one_key, one_value in group_value.items():
            # print(one_key)
            column = 2
            worksheet.write(row, column - 1, one_key, normal_format)
            for one in one_value:
                worksheet.write(row, 0, row - 1, normal_format)
                for key, value in one.items():
                    if key == 'len':
                        # 总分	评分	组别	主管 共计4个
                        column = column + value + 4
                        continue
                    if key not in except_field:
                        # print(row, column, key, value)
                        worksheet.write(row, column, value, normal_format)
                        column += 1
            row += 1
    workbook.close()
    pass

def to_mail():
    result = InformationEmployees.objects.filter(status=True).order_by("enter_days").all()
    print(result)
    if len(result):
        from_email = settings.DEFAULT_FROM_EMAIL
        # subject 主题 content 内容 to_addr 是一个列表，发送给哪些人
        print(from_email, settings.conf.get(section='email', option='to_addr').split(','))
        print(type(settings.conf.get(section='email', option='to_addr').split(',')))
        content = render(None, template_name='research/email.html',
                         context={'emp_list': result, }).getvalue().decode("utf-8")
        msg = EmailMultiAlternatives("{today}的新人培养调查名单".format(today=datetime.date.today()),
                                     content, from_email,
                                     settings.conf.get(section='email', option='to_addr').split(','))
        msg.content_subtype = "html"
        # 添加附件（可选）
        # msg.attach_file('./xxx.pdf')
        # 发送
        msg.send()
    pass