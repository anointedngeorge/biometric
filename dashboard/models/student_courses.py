from django.db import models
from core.core import CoreDb


SUBJECTS_LIST_DISPLAY = ['code','name','unit']
class Subjects(CoreDb):
    code = models.CharField(max_length=250, verbose_name='course code', null=True)
    name = models.CharField(max_length=250, verbose_name='course title', null=True)
    unit = models.IntegerField(default=1, verbose_name='credit unit', null=True)

    class Meta:
        verbose_name = 'Course listing'
        verbose_name_plural = 'Course Listing'
    
    def __str__(self) -> str:
        return f"{self.name}"


STUDENT_SUBJECT_LIST_DISPLAY = ['user','code','subject', 'unit','department', 'levels', 'semester']
class RegisterStudentSubject(CoreDb):
    user = models.ForeignKey("authuser.StudentModel", 
            verbose_name='student', 
            on_delete=models.CASCADE, 
            null=True, 
            related_name='student_courses'
        )
    subject = models.ForeignKey("dashboard.Subjects", on_delete=models.CASCADE, null=True, 
                                related_name='student_subjects', verbose_name='Courses')
    
    department = models.ForeignKey("dashboard.DepartmentListing", on_delete=models.CASCADE, null=True, 
                                related_name='student_department')
    code = models.CharField(max_length=250, verbose_name='course code', null=True, editable=False)
    unit = models.IntegerField(default=1, verbose_name='credit unit', null=True, editable=False)
    levels = models.ForeignKey("dashboard.Levels", on_delete=models.CASCADE, 
                               null=True, related_name='student_course_level_rel')
    semester =  models.CharField(max_length=500, default='first', choices=[
                                            ('first','First Semester'), 
                                            ('second', 'Second Semester'),
                                            ('third', 'Third Semester'),
                                        ], null=True)

    class Meta:
        verbose_name = 'Student Course'
        verbose_name_plural = 'Student Courses'
    
    def __str__(self) -> str:
        return f"{self.user} - {self.subject}"
    

# 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

