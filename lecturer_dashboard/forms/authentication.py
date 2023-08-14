from django import forms

from django.contrib.auth.forms import AuthenticationForm


from authuser.models import *

class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def confirm_login_allowed(self, user):
        from django.core.exceptions import PermissionDenied
        if user.is_superuser:
            raise PermissionDenied("Superusers are not expected to access this page. ")
        if user.is_anonymous:
            raise PermissionDenied("You're not permitted to access this page.")
        if not user.account_type == 'lecturer':
            raise PermissionDenied("You must be lecturer!")
        
        roles = user.account_type
        permission_group = Group.objects.get(name=roles)
        user.groups.add(permission_group)


class AuthenticationRegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"
        exclude = ('groups','user_permissions','is_active','is_staff','is_superuser','last_login','password')







# class BusinessRegistrationForm(forms.ModelForm):

#     class Meta:
#         model = Business
#         fields = ['first_name','last_name']
#         # exclude = ('groups','user_permissions','is_active','is_staff','is_superuser','last_login','password',)




# as_div
# as_p
# as_table
# as_ul
# base_fields
# changed_data
# clean
# confirm_login_allowed
# declared_fields
# default_renderer
# error_messages
# errors
# field_order
# full_clean
# get_context
# get_initial_for_field
# get_invalid_login_error
# get_user
# has_changed
# has_error
# hidden_fields
# is_multipart
# is_valid
# media
# non_field_errors
# order_fields
# prefix
# render
# template_name
# template_name_div
# template_name_label
# template_name_p
# template_name_table
# template_name_ul
# use_required_attribute
# visible_fields