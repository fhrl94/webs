# 新员工培养调查-线上化

- [更新](#更新)

- [bug](#bug)

- [使用说明](#使用说明)

- [文件说明](#文件说明)

- [背景介绍](#背景介绍)

- [进度列表](#进度列表)

## 更新

- 2018.1.25 【进度列表-6】已完成；调整了【home】页面继承方式；

- 2018.1.24 调整【home.js】、【home.html】修复bug-4；过滤器顺序调整；背景介绍整理；

- 2018.1.23 【优化】已完成；bug-2、3修复；使用 jQuery 【home.js】调整最终页面；新增【需求-8】

- 2018.1.22 优先级更改为【优化】、 6 、 5 、7  ，以及bug-1修复

- 2018.1.10 已完成[进度列表](#进度列表)中的2、3

- 2018.1.9 [进度列表](#进度列表)中的2、3、5、6、7 以及【优化】待完成。
2、3 需在 **2018.1.16** 前完成。
5、6、7 以及【优化】按先后顺序完成。

## bug

1. 客发问卷有选填项，允许为空。
出现[异常](https://github.com/fhrl94/webs/blob/eb8451a3db93052b0db1fda0e93b1f64c05e4e66/research/views.py#L77-L78)

2. 通过URL可以直接访问下一期问卷（视图 index_view() 需要检查是否有问卷)

3. pdf、excel 数据异常修复

4. home 页面，不需要填写的问卷，不应该有链接

## 使用说明

安装 uWSGI

`pip3.6 install uWSGI`

安装 Nginx

`yum install epel-release`

`yum install python-devel nginx`

后续 Linux 操作
```
需要是使用 Django 命令进行收集
在setting.py 文件中增加 
            STATIC_URL = '/static/'
            STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
            
python manage.py collectstatic

使用软连接命令 
ln -s 【research_nginx.conf】的绝对路径 /etc/nginx/conf.d/XXX.conf

Nginx 操作命令
/bin/systemctl restart  nginx.service     重启 Nginx 服务 对配置进行更改后需要重启
/bin/systemctl start  nginx.service       启动 Nginx 服务
systemctl status nginx.service -l          查看 Nginx 错误信息

```

## 文件说明
- webs/.
    * research/.
        * static/ .
            * css/.
                * login.css 自定义 css 文件, 用于登录界面
            * jQuery/.
                * home.js 【home 页面】实现列表展示
        * templates/.
            * research/.
                * login.html 登录界面模板 表单为 UserForm
                * base.html 基础模板， 继承了 Django-bootstrap3 中的模板
                * form.html 问卷表单模板，继承了 base.html ，使用 CustomerXXXForm 和 SellXXXForm 表单
                * form_dump.html 导出问卷表单模板， 与 form.html 相似（无提交按钮以及bootstrap资源指向）
                * home_base.html 导航栏模板，继承了 base.html
                * 404.html 出错模板，继承了 home_base.html ，非 admin 和 research 的应用、错误网站、异常， 均指向此
                * home.html 主页，继承了 home_base.html ， 登录后指向此
                * logout.html 登出，继承了 home_base.html ， 注销当前使用账户 
                * change_pwd.html 密码修改， 继承了 home_base.html 
        * admin.py 后台页面定制， 筛选、执行动作等待
        * forms.py 表单设计， 包含 UserForm 、ChangePwdForm 、 CustomerXXXForm 、 SellXXXForm
        * models.py 数据库设计， 包含 InformationEmployees 、 CustomerXXX 、 SellXXX
        * urls.py URL 表， index 、 home、 login 、 logout 、 change_pwd 、 error_404
        * views.py 包含业务视图 index_view 、 home_form 、 user_login 、 user_logout 、 change_pwd 、 error_404 </br>
        后台动作 auto_cal 、 html_download 、 excels_download </br>
        以及动作调用的函数 temp_form 、 reg_exp 、 zip_pack 、 clear_temp 、 file_iterator 、 download_file 、 excel_write
    * webs/.
        * settings.py 新增APP 'bootstrap3' (django-bootstrap3)
        ```
            LANGUAGE_CODE = 'zh-hans'
            TIME_ZONE = 'Asia/Shanghai'
            STATIC_URL = '/static/'
            STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
            # 这个是默认设置，Django 默认会在 STATICFILES_DIRS中的文件夹 和 各app下的static文件夹中找文件
            # 注意有先后顺序，找到了就不再继续找了
            STATICFILES_FINDERS = (
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "django.contrib.staticfiles.finders.AppDirectoriesFinder")
        ```
        * urls.py 总的 URL 表
        ```
            url(r'^research/', include('research.urls')),
        ```
        * wsgi.py 
    * manage.py
    * README.md 说明文件
    * research_nginx.conf Nginx 配置文件
    * research_uwsgi.ini uWSGI 配置文件
        
## 背景介绍

新员工培养问卷调查，是针对运值和客发体系员工；入职后，通过周期的培养，对员工进行实名的调查反馈。该问卷主要分为【沟通与通知】、【数据录入与汇总】。

一、沟通与通知：

	1、根据线下表，通知到期员工填写问卷。
	（手动查看到期时间，逐一电话通知到期员工，告诉他们需要填写的问卷期数以及集中填写问卷的时间）
	
	2、准备问卷
	（打印表单，并手写上员工姓名和所属部门及负责人姓名，通知员工填写问卷）
	
二、数据录入与汇总：

	1、问卷调查结果录入
	
	   a.找到对应调查人的问卷表单，录入最新的个人信息（包括组别、直属上级、所属阶段、入职天数等）和分数结果。
	   
	   b.以组别+直属上级为单位，对问卷调查表进行汇总，并发送邮件至考核人上级。
	   
	2、数据汇总
	
	   a.将各个阶段的数据明细录入汇总表。
	   
业务需求：

    1）员工线上填写问卷（一.2））【已完成】
    
    2）问卷调查的结果自动生成文件并打包为zip文件（二.1.a）【已完成】
    
    3）问卷调查的结果汇总为excel表格（二.2.a） 【已完成】
    
    4）邮件通知专员【到期员工列表】（一.1） 【待完成】
    
    5）实现实名调查，需要登录功能、以及修改密码 【密码修改待完成】
    
    可能涉及：
    
    6）问卷调整
    
    7）填写错误进行修改	   
        
## 进度列表

1. 员工通过账号、密码来登录、退出登录，在线填写问卷

2. 填写的问卷能在线导出（美观）， 同时按下列方式打包

    * 【新人培养调查问卷原始表】
        * 【部门-直接上级】（新增部门，区别可能存在兼职人员）
            * 【员工表单-期数-主管name】
    
3. 填写的数据能汇总，导出 excel 表（增加组别）,下图为运值样表

<table>
    <col span="60">
    <tr>
        <td></td>
        <td></td>
        <td colspan="14" align="center">第1问卷调查</td>
        <td colspan="14" align="center">第2问卷调查</td>
        <td colspan="14" align="center">第3问卷调查</td>
        <td colspan="21" align="center">第4问卷调查</td>
    </tr>
    <tr>
        <td>序号</td>
        <td>姓名</td>
        <td>问题1</td>
        <td>问题2</td>
        <td>问题3</td>
        <td>问题4</td>
        <td>问题5</td>
        <td>问题6</td>
        <td>问题7</td>
        <td>问题8</td>
        <td>问题9</td>
        <td>问题10</td>
        <td>总分</td>
        <td>评分</td>
        <td>组别</td>
        <td>主管</td>
        <td>问题1</td>
        <td>问题2</td>
        <td>问题3</td>
        <td>问题4</td>
        <td>问题5</td>
        <td>问题6</td>
        <td>问题7</td>
        <td>问题8</td>
        <td>问题9</td>
        <td>问题10</td>
        <td>总分</td>
        <td>评分</td>
        <td>组别</td>
        <td>主管</td>
        <td>问题1</td>
        <td>问题2</td>
        <td>问题3</td>
        <td>问题4</td>
        <td>问题5</td>
        <td>问题6</td>
        <td>问题7</td>
        <td>问题8</td>
        <td>问题9</td>
        <td>问题10</td>
        <td>总分</td>
        <td>评分</td>
        <td>组别</td>
        <td>主管</td>
        <td>问题1</td>
        <td>问题2</td>
        <td>问题3</td>
        <td>问题4</td>
        <td>问题5</td>
        <td>问题6</td>
        <td>问题7</td>
        <td>问题8</td>
        <td>问题9</td>
        <td>问题10</td>
        <td>问题11</td>
        <td>问题12</td>
        <td>问题13</td>
        <td>问题14</td>
        <td>问题15</td>
        <td>问题16</td>
        <td>问题17</td>
        <td>总分</td>
        <td>评分</td>
        <td>组别</td>
        <td>主管</td>
    </tr>
    </table>
    
4. 2种类型问卷

5. 当入职天数到达下一周期，发送此人员名单邮件至业务人员

6. 员工可以修改密码

7. 员工通知业务人员后，可以修改历史数据

8. 记录员工填写问卷的时间，维护线下表（暂定）

优化：

员工的问卷调查显示具体情况，显示如下

<table>
    <tbody>
        <tr>
            <td>第1期新员工调查问卷</td>
            <td><div class="bool" id="wj1">已完成</div></td>
        </tr>
        <tr>
            <td>第2期新员工调查问卷</td>
            <td><div class="bool" id="wj2">已完成</div></td>
        </tr>
        <tr>
            <td>第3期新员工调查问卷</td>
            <td><div class="bool" id="wj3">已完成</div></td>
        </tr>
        <tr>
            <td>第4期新员工调查问卷</td>
            <td><div class="bool" id="wj4">已完成</div></td>
        </tr>
        <tr>
            <td>第5期新员工调查问卷</td>
            <td><div class="bool" id="wj5">已完成</div></td>
        </tr>
        <tr>
            <td>第6期新员工调查问卷</td>
            <td><div class="bool" id="wj6">已完成</div></td>
        </tr>
    </tbody>
<table>