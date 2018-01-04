from django.contrib import admin

# Register your models here.
from research.models import InformationEmployees
from research.views import auto_calculate, form_print, excel_download


class InformationEmployeesAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'group', 'superior_name', 'next_section', 'tel']
    exclude = ['next_section', 'consult_section', 'enter_days', ]
    search_fields = ('name',)
    actions = ['auto_cal', 'html_download', 'excels_download', ]
    list_filter = ['next_section', 'superior_name', 'department', 'group', 'status']
    ordering = ('-enter_days',)
    list_editable = ('group', 'tel',)

    def auto_cal(self, request, queryset):
        return auto_calculate(None)
        pass

    def html_download(self, request, queryset):
        return form_print(request, queryset)
        pass

    def excels_download(self, request, queryset):
        return excel_download(request, queryset)

    auto_cal.short_description = "自动计算入职天数、下个填写阶段"
    html_download.short_description = "html打包下载"
    excels_download.short_description = "excel表下载"


admin.site.register(InformationEmployees, InformationEmployeesAdmin)
# 设置站点标题
admin.site.site_header = '新人线上调查管理系统'
admin.site.site_title = '新人线上调查'  # TODO 数据导出（分原始表单（HTML）、原始数据导出（excel））
