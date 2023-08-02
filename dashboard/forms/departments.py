from django import forms
from dashboard.models.departments import Departments



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ('department','student')
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Department.','required':True}),
        }