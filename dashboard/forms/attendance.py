from django import forms
from django.db.models.query_utils import Q
from django.contrib.auth.forms import UserCreationForm
from dashboard.models import CreateAttendance
from django.forms.fields import MultipleChoiceField
import uuid

class AttendanceForm(forms.ModelForm):
    # excluded_fields =  ['email', 'password']
    def __init__(self, *args, attributes=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes = attributes

    class Meta:
        model = CreateAttendance
        fields = "__all__"
        exclude = ['created','attributes','total_number_students','code']
        widgets = {
            'lecturer': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'levels': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'time_elapsed':forms.NumberInput(attrs={'class': 'form-control'}),
            
         }
        

    # def clean(self):
    #     cleaned_data = super().clean()
    #     for field_name in self.excluded_fields:
    #         if field_name in cleaned_data:
    #             cleaned_data.pop(field_name)
    #     # Perform any additional cleaning/validation if needed
    #     return cleaned_data
    

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.attributes = self.attributes
        
        if commit:
            instance.save()
        return instance

