
from django.contrib import admin
from .models import Student, Class

# def activate_students(modeladmin, request, queryset):
#     queryset.update(status=True)
#
# def deactivate_students(modeladmin, request, queryset):
#     queryset.update(status=False)
#
# class StudentAdmin(admin.ModelAdmin):
#     actions = [activate_students, deactivate_students]

# admin.site.register(Student, StudentAdmin)

admin.site.register(Class)
