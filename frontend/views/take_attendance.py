from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

TEMPLATE = 'front'

import face_recognition
# import cv2
import numpy as np
import csv
import os
from datetime import datetime
import face_recognition



def takeAttendance(request):
    if request.method == 'POST':
        files = request.FILES['photoFile'].read()
    return HttpResponse('Attendance taking')