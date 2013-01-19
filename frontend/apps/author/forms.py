from apps.practice.models import *
from tinymce.widgets import TinyMCE

from django import forms

class ProblemForm(forms.ModelForm):
        class Meta:
                model = Problem
                widgets = {
                                'description' : TinyMCE(attrs={'cols': 80, 'rows': 30, } ),
                                }
