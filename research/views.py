import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from research.forms import *
from research.models import InformationEmployees

section_list = ['section_one', 'section_two', 'section_three', 'section_four', 'section_five', 'section_six', ]

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
    form_customer = [CustomerOneForm, CustomerTwoForm, CustomerThreeForm, CustomerFourForm, CustomerFiveForm,
                     CustomerSixForm]
    form_sell = [SellOneForm, SellTwoForm, SellThreeForm, SellFourForm]
    if user_emp.department == "y" and user_emp.current_section[0] == "y":
        form = form_customer[int(user_emp.current_section[1]) - 1]
    elif user_emp.department == "k" and user_emp.current_section[0] == "k":
        form = form_sell[int(user_emp.current_section[1]) - 1]
    elif user_emp.current_section == 'completed':
        return error_404(request, "已完成所有的调查")
    # TODO 当前无问卷调查
    else:
        return error_404(request, "部门信息错误，请联系管理员")
    if request.method == 'POST':
        user_form = form(request.POST)
        if user_form.is_valid():
            #  数据写入
            new_form = user_form.save(commit=False)
            new_form.department = user_emp.department
            new_form.group = user_emp.group
            # 新增【直接上级】、【当前阶段】、【入职天数】、【联系方式】、【入职日期】
            new_form.superior_name = user_emp.superior_name
            new_form.current_section = user_emp.current_section
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
            print(section_list[int(user_emp.current_section[1]) - 1])
            print(getattr(user_emp, section_list[int(user_emp.current_section[1]) - 1]))
            setattr(user_emp, section_list[int(user_emp.current_section[1]) - 1], True)
            user_emp.save()
            # 保存完毕后进行计算
            auto_calculate(user_emp.pk)
            return HttpResponseRedirect(reverse(home_form))
    else:  # 当正常访问时
        # user_form = CustomerOneForm()
        user_form = form()
    return render(request=request, template_name='research/form.html', context={
        'user_form': user_form, 'user_emp': user_emp, 'today':datetime.date.today(),
        'num':int(user_emp.current_section[1])})
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
    if user_emp.current_section == "completed":
        body = '您已完成所有问卷'
    elif user_emp.current_section <= user_emp.consult_section:
        # print("当前填写第{num}期".format(num=int(user_emp.current_section[1])))
        research_exist = True
        num = int(user_emp.current_section[1])
    return render(request, template_name='research/home.html', context={
        'research_exist':research_exist, 'num':num, 'body':body
    })


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
    return render(request, template_name='research/404.html', context={
        'error_body':error_body,
    })
    pass

# TODO 实现装饰器
def auto_calculate(ID):
    """
    计算 【入职天数】、【当前阶段】、【理论阶段】
    :return:
    """
    customer = {'161': 'y6', '133': 'y5', '105': 'y4', '77': 'y3', '49': 'y2', '28': 'y1', '-1':'y0', }
    sell = {'90': 'k4', '60': 'k3', '30': 'k2', '14': 'k1', '-1':'k0', }
    if ID == None:
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
                break
            # print(one.consult_section)
        # 计算当前阶段
        for j, consult in enumerate(section_list):
            # print(getattr(user_emp, one))
            if not getattr(one, consult):
                # 部门为客发超过4期，即完成
                if one.department == "k" and j >= 4:
                    one.current_section = "completed"
                    break
                # 部门为客发，且未完成到第3期 or
                # 部门为运值，且未全部完成（共6期）
                # print(one.department + str(j+1))
                one.current_section = one.department + str(j + 1)
                break
            # 均完成，即运值已全部完成
            else:
                one.current_section = "completed"
        one.save()
    # print(type(result))
    pass
