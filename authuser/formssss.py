from django import forms
from django.db.models.query_utils import Q
from django.contrib.auth.forms import UserCreationForm
from authuser.models import User
from django.forms.fields import MultipleChoiceField
from .models import *
# from plugins.generator import generator

class userRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = '__all__'
        # exclude = ['password2']
        
    def save(self, commit=True):
        try:
            user = super(userRegistrationForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.is_staff = True
                user.is_active = True
                # user.code = generator(length=4)
                user.save()
            return user
        except Exception as e:
            print(e)




