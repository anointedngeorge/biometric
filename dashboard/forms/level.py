from django import forms
from dashboard.models.level import *



class LevelForm(forms.ModelForm):
    class Meta:
        model = Levels
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'New Level.','required':True}),
        }