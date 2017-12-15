from django.contrib import admin

# Register your models here.
from research.models import InformationEmployees

admin.site.register(InformationEmployees)


# TODO 数据导出（分原始表单（HTML）、原始数据导出（excel））
# TODO 排序
# TODO 搜索