from django.contrib import admin
from dashboard.models.departments import *



@admin.register(Faculty)
class FacultyListingAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY_FACULTY_LISTING

@admin.register(DepartmentListing)
class DepartmentListingAdmin(admin.ModelAdmin):
    list_display = LIST_DISPLAY_DEPARTMENT_LISTING



# @admin.register(Departments)
# class DepartmentsAdmin(admin.ModelAdmin):
#     list_display = LIST_DISPLAY_DEPARTMENT
    