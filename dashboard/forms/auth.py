from django import forms

class LoginForm(forms.Form):
    password = forms.CharField(max_length=100)
    username = forms.EmailField()
    
    class Meta:
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control', 'type':'password'}),
            'username': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }




# class MyModelForm(forms.ModelForm):
#     class Meta:
#         model = MyModel
#         fields = ['name', 'email', 'age']