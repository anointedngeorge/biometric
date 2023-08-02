from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from dashboard.forms.auth import *
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import datetime
import calendar
from authuser.forms import LecturerForm,StudentForm
from dashboard.forms.attendance import AttendanceForm
from dashboard.models.attendance import CreateAttendance

TEMPLATE = settings.ADMIN_DASHBOARD_TEMPLATE


def getCurrentDate():
    current_date = datetime.datetime.now()
    return current_date

def getCurrentDay():
    current_date = datetime.datetime.now()
    return current_date.day
    

def getCurrentMonth():
    current_date = datetime.datetime.now()
    return current_date.month


def daysInMonth(year=2023, month = 5):
    obj = []
    num_days = calendar.monthrange(year, month)[1]
    day_names = [calendar.day_name[calendar.weekday(year, month, day)] for day in range(1, num_days + 1)]
    for day, name in enumerate(day_names, start=1):
        # print(f"Day {day}: {name}")
        obj.append({'day':day, 'name':name})
    return obj
    


@login_required
def index(request):
    return render(request, f"{TEMPLATE}/index.html")


@login_required
def page(request):
    query = request.GET.dict()
    pagename  = query.get('pagename')
    folder  = query.get('folder')
    form = query.get('form')
    user = query.get('user')
    context = {}
    context['page_title'] = folder
    context['current_month_name'] = 'May'
    context['current_date'] = getCurrentDate()
    context['current_day'] = getCurrentDay()
    context['user'] = user
    context['current_month'] = getCurrentMonth()
    context['range_number'] = daysInMonth(month=getCurrentMonth())
    context['objects'] = CreateAttendance.objects.all()
    context['form'] = eval(form)() if form != None else LecturerForm()
    return render(request, f"{TEMPLATE}/{folder}/{pagename}.html", context=context)

# @login_required
def auth_login(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form['username'].value()
        password = form['password'].value()
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        else:
            return redirect('/')
    return render(request, f"{TEMPLATE}/login.html", context=context)


def auth_logout(request):
    logout(request)
    return render(request, f"{TEMPLATE}/login.html")
        