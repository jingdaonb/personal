from django.contrib import admin

# Register your models here.

from app01 import models

admin.site.register(models.UserInfo)
admin.site.register(models.Menu)
admin.site.register(models.Permission)
admin.site.register(models.Role)

admin.site.register(models.Customer)
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)
admin.site.register(models.ClassStudyRecord)
admin.site.register(models.Student)
admin.site.register(models.StudentStudyRecord)
