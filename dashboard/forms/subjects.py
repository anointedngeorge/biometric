from django import forms
from dashboard.models.student_courses import *



class SubjectsForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Subject name...','required':True}),
            'descriptions': forms.EmailInput(attrs={'placeholder': 'description...'}),
        }