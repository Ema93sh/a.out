from models import *
from apps.tinymce.widgets import TinyMCE

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class SubmissionForm(forms.Form):
	language =  forms.ModelChoiceField(Language.objects.all())
	userCode = forms.FileField()

	def __init__(self, *args, **kwargs):
		problem = kwargs.pop('problem', None)
	        super(SubmissionForm, self).__init__(*args, **kwargs)
		if problem:
			self.fields['language'].queryset= problem.languages

class ProblemForm(forms.ModelForm):
	class Meta:
		model = Problem
		widgets = {
				'description' : TinyMCE(attrs={'cols': 80, 'rows': 30, } ),
				}

	
