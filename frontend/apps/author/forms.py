from apps.practice.models import *
from apps.database_files.models import *
from tinymce.widgets import TinyMCE
from django.forms.formsets import formset_factory


from django import forms

class ProblemForm(forms.ModelForm):
        class Meta:
                model = Problem
                widgets = {
                                'description' : TinyMCE(attrs={'cols': 80, 'rows': 30, } ),
                                }
class TestCaseForm(forms.Form):
   inputFile=forms.FileField()
   outputFile=forms.FileField()
   
