from django.db import models
from core.core import CoreDb


LIST_DISPLAY_FACULTY_LISTING = ['name']
class Faculty(CoreDb):
    name = models.CharField(max_length=350)

    def __str__(self):
        return f"{self.name}"
    
    
    class Meta:
        verbose_name = 'Faculty Listing'
        verbose_name_plural = 'Faculty Listing'



LIST_DISPLAY_DEPARTMENT_LISTING = ['name', 'faculty']
class DepartmentListing(CoreDb):
    name = models.CharField(max_length=350)
    faculty = models.ForeignKey("dashboard.Faculty", on_delete=models.CASCADE,  
                                related_name='department_listing_faculty_rel', null=True)

    def __str__(self):
        return f"{self.name} - {self.faculty}"
    
    
    class Meta:
        verbose_name = 'Department Listing'
        verbose_name_plural = 'Department Listings'

    



LIST_DISPLAY_DEPARTMENT = ['department','student']
class Departments(CoreDb):
    department = models.ForeignKey("dashboard.DepartmentListing", on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey("authuser.StudentModel", on_delete=models.CASCADE, null=True, blank=True)
    # description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self) -> str:
        return f"{self.department}"