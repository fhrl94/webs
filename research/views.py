from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from research.forms import *
from research.models import InformationEmployees


@login_required(login_url="login")
def index_view(request):
    # return render(request=request, template_name='research/form.html')
    user = getattr(request, 'user', None)
    # print(user.id)
    # print(user)
    # print(InformationEmployees.objects.filter(emp_user = user.id))
    # 获取当前登录用户信息
    try:
        user_emp = InformationEmployees.objects.filter(emp_user=user.id).get()
    except:
        return HttpResponse("用户关联错误，请联系管理员")
    # 根据用户信息（部门、当前阶段）确定相应 表单
    model_customer = [CustomerOneForm, CustomerTwoForm, CustomerThreeForm, CustomerFourForm, CustomerFiveForm,
                      CustomerSixForm]
    model_sell = [SellOneForm, SellTwoForm, SellThreeForm, SellFourForm]
    if user_emp.department == "y" and user_emp.current_section[0] == "y":
        Form = model_customer[int(user_emp.current_section[1]) - 1]
    elif user_emp.department == "k" and user_emp.current_section[0] == "k":
        Form = model_sell[int(user_emp.current_section[1]) - 1]
    else:
        return HttpResponse("部门信息错误，请联系管理员")
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            # TODO 数据写入
            # name = form.cleaned_data['user_name']
            # body = form.cleaned_data['body']
            return HttpResponseRedirect(reverse(home_form))
    else:  # 当正常访问时
        # form = CustomerOneForm()
        form = Form()
    return render(request=request, template_name='research/form.html', context={'form':form, 'user_emp':user_emp})
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
    return render(request, template_name='research/home.html')

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
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = UserForm()
    return render(request, template_name='research/login.html', context={'form': form})

def user_logout(request):
    logout(request)
    return render(request, template_name='research/logout.html')
    pass
