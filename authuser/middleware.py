from django.http import HttpResponse
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect,render, resolve_url
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import Group


current_user = []

class CheckUserSiteMiddleware(MiddlewareMixin):
     def process_request(self, request):
         user = request.user
         try:
            if (user.is_authenticated):
               # print('Yes authenticated')
               if  (user.is_superuser) and (request.path.startswith('/admin/')):
                  pass
               else:
                  request.session.flush()
                  return HttpResponseForbidden()
         except Exception as e:
             return HttpResponse(e)


class SetLoggedinUserRoleAsGroup(MiddlewareMixin):
     def process_request(self, request):
        user = request.user
        try:
             if (user.is_authenticated) and not ( user.is_superuser):
                 roles = request.user.roles.id
                 permission_group = Group.objects.get(id=roles)
                 user.groups.add(permission_group)
               #   print(user.groups.all())
        except Exception as e:
           return e
        

class LoggedInUserMiddleware(MiddlewareMixin):
    '''
      Insert this middleware after django.contrib.auth.middleware.AuthenticationMiddleware
    '''
    def process_request(self, request):
        if request.user.is_authenticated:
           current_user.clear()
           current_user.append(request.user)
           
         
         
