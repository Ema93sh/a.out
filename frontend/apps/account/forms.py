from apps.practice.models import *
from apps.database_files.models import *
from apps.captcha.fields import *
from tinymce.widgets import TinyMCE
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User


from django import forms

class registrationForm(forms.Form):
   username=forms.CharField()
   password = forms.CharField(widget=forms.PasswordInput)
   confirmPassword=forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
   captcha = ReCaptchaField()
   widgets={
      'password' :forms.PasswordInput(),
      }
