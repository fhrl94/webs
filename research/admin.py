from django.contrib import admin

# Register your models here.
from research.models import InformationEmployees, WriteHistory
from research.views import auto_calculate, form_print, excel_download, to_mail


class InformationEmployeesAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'group', 'superior_name', 'next_section', 'tel', 'pwd_status', ]
    exclude = ['next_section', 'consult_section', 'enter_days', ]
    search_fields = ('name',)
    actions = ['auto_cal', 'html_download', 'excels_download', 'to_mail_test']
    list_filter = ['status', 'department', 'pwd_status', 'emp_status', 'next_section', 'superior_name', 'group', ]
    ordering = ('-enter_days',)
    list_editable = ('group', 'tel', 'superior_name')

    def auto_cal(self, request, queryset):
        return auto_calculate(None)
        pass

    def html_download(self, request, queryset):
        return form_print(request, queryset)
        pass

    def excels_download(self, request, queryset):
        return excel_download(request, queryset)

    def to_mail_test(self, request, queryset):
        to_mail()
        pass

    auto_cal.short_description = "自动计算入职天数、下个填写阶段"
    html_download.short_description = "html打包下载"
    excels_download.short_description = "excel表下载"
    to_mail_test.short_description = '邮件发送'

class WriteHistoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'enter_date', 'current_section', 'employees', ]
    search_fields = ('name',)
    list_filter = ['current_section', 'enter_date', ]
    ordering = ('-enter_date',)
    date_hierarchy = 'enter_date'
    actions = ['html_download', 'excels_download']

    def html_download(self, request, queryset):
        return form_print(request, queryset, type=True)
        pass

    def excels_download(self, request, queryset):
        list = []
        for one in queryset:
            print(type(one.employees))
            list.append(one.employees)
        list_tmp = sorted(set(list), key=list.index)
        return excel_download(request, list_tmp)

    html_download.short_description = "html打包下载"
    excels_download.short_description = "excel表下载"

admin.site.register(InformationEmployees, InformationEmployeesAdmin)
admin.site.register(WriteHistory, WriteHistoryAdmin)
# 设置站点标题
admin.site.site_header = '新人线上调查管理系统'
admin.site.site_title = '新人线上调查'  # 数据导出（分原始表单（HTML）、原始数据导出（excel））
