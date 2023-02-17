from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    #first_name = forms.CharField(max_length=63, label='First name')
    # last_name = forms.CharField(max_length=63, label='Last name')
    username = forms.CharField(max_length=63, label='Username')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')


# authentication/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# class SignupForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = ('username', 'email', 'first_name', 'last_name')  
        

SERVICE_CHOICES = (
    ("Servic A", "Servic A"),
    ("NServic B", "Servic B"),
    ("Servic C", "Servic C"),
    ("Servic D", "Servic D"),
    )
TIME_CHOICES = (
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Servic A")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3-3:30 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"