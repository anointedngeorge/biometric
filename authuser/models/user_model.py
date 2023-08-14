from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin,
    BaseUserManager,
    UserManager
)
import uuid
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


GROUP_ROLES = [
    ('staff','Staff'),
    ('customer','Customer')
]

# Salutation - Mr, Mrs, Mr and Mrs, miss, Dr, Sir, Madam


class CustomUserManager(UserManager):
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a vaild email address")

        email = self.normalize_email(email)
        user =  self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_superuser",False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)
        

class User(AbstractBaseUser, PermissionsMixin):

    class AccountType(models.TextChoices):
        none =  "","-----"
        student =  "student","Student"
        lecturer = "lecturer","Lecturer"
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(('email address'), unique=True, error_messages="Email Already Taken")
    username = models.CharField(max_length=300, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    roles = models.ForeignKey(Group, on_delete=models.CASCADE, 
                              blank=True, null=True,
                              related_name='roles_rel_group')
    
    bio_capture = models.CharField(max_length=500, blank=True, null=True)
    bio_capture2 = models.CharField(max_length=500, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=timezone.now())
    last_login = models.DateTimeField(blank=True, null=True)

    account_type = models.CharField(max_length=250, 
                                    choices=AccountType.choices, 
                                    default=AccountType.none)
    # account_type2 = models.CharField(max_length=250, 
    #                                 choices=AccountType.choices, 
    #                                 default=AccountType.none)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def get_user(self):
        user =None
        if self.account_type == 'student':
            student = self.studentmodel
            user =  f"{student.surname} {student.first_name} {student.last_name}"
        elif self.account_type == 'lecturer':
            student = self.lecturermodel
            user =  f"{student.surname} {student.first_name} {student.last_name}"
        return user
    
    def get_student_attendance_count(self):
        student = self.studentmodel.attendance_taken_student.filter(student_id=self.id).count()
        return student
    

    def get_lecturer_attendance_count(self):
        try:
            student = self.Lecturermodel.attendance_lecturer_related.filter(lecturer_id=self.id).count()
            return student
        except:
            return 0

    def __str__(self) -> str:
        if self.username:
            return f"{self.username} - {self.email}"
        return 'Admin'

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)


 
