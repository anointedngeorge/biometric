from django import forms
from django.db.models.query_utils import Q
from django.contrib.auth.forms import UserCreationForm
from authuser.models import LecturerModel, User
from django.forms.fields import MultipleChoiceField
import uuid


class LecturerForm(forms.ModelForm):


    def __init__(self, *args, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id

    class Meta:
        model = LecturerModel
        fields = "__all__"
        exclude = ['created','user_permissions','groups','is_superuser','code',
                   'last_login','is_active','is_staff','bio_capture','bio_capture2','roles','picture_url']
        widgets = {
            'salutation': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
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
        instance.is_active = True
        instance.is_staff =  True
        return super().save(commit=True)

