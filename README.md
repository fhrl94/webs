# 新员工培养调查

## 更新


## 使用

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
        * templates/.
            * research/.
                * login.html 登录界面模板 表单为 UserForm
                * base.html 基础模板， 继承了 Django-bootstrap3 中的模板
                * 404.html 出错模板， 非 admin 和 research 的应用、错误网站、异常， 均指向此
                * form.html 问卷表单模板， 使用 CustomerXXXForm 和 SellXXXForm 表单
                * form_dump.html 导出问卷表单模板， 与 form.html 相似，细节有所改变
                * home.html 主页模板， 登录后指向此
                * logout.html 登出模板， 注销当前使用账户 
        * admin.py 后台页面定制， 筛选、执行动作等待
        * forms.py 表单设计， 包含 UserForm 、 CustomerXXXForm 、 SellXXXForm
        * models.py 数据库设计， 包含 InformationEmployees 、 CustomerXXX 、 SellXXX
        * urls.py URL 表， index 、 home、 login 、 logout 、 error_404
        * views.py 包含业务视图 index_view 、 home_form 、 user_login 、 user_logout 、 error_404 </br>
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
        
        
        
## 需求：

1. 员工通过账号、密码，在线填写问卷

2. 填写的问卷能在线导出（美观）， 同时按列方式打包

    * 【新人培养调查问卷原始表】
        * 【部门-直接上级-人数】
            * 【员工-直接上级-分数】
                * 【员工表单-期数】
    
3. 填写的数据能汇总，导出 excel 表

4. 2种类型问卷

## 实现思路：




