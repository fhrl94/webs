from django.contrib import admin

# Register your models here.
from research.models import InformationEmployees
from research.views import auto_calculate


class InformationEmployeesAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'group', 'superior_name', 'current_section', 'tel']
    exclude = ['current_section', 'consult_section', 'enter_days',]
    search_fields = ('name',)
    actions = ['auto_cal', ]

    def auto_cal(self, request, queryset):
        return auto_calculate(None)
        pass

    auto_cal.short_description = "自动计算入职天数、当前阶段"


admin.site.register(InformationEmployees, InformationEmployeesAdmin)

# TODO 数据导出（分原始表单（HTML）、原始数据导出（excel））


