from django import forms
from dashboard.models import Courses



class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = "__all__"
        exclude = ['created']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control','required':True}),
            'subject': forms.Select(attrs={'class': 'form-control', 
                                    'required':True}),
            'lecturer': forms.Select(attrs={'class': 'form-control', 
                                    'required':True}),
            'course': forms.Select(attrs={'class': 'form-control', 
                                    'required':True}),
            'levels': forms.Select(attrs={'class': 'form-control', 
                                    'required':True}),

        }