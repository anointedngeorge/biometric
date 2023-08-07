from dashboard.models import Subjects
from authuser.forms import StudentForm, LecturerForm
from frontend.models import *

def processor(request):
    


    return {
        'processor_subject':Subjects.objects.all(),
        'studentform':StudentForm,
        'lecturerform':LecturerForm,
        'sliders':Slider.objects.all(),
        'about':About.objects.all().first(),
        'logo_url':Logo.objects.all().first(),
    }