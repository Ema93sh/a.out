from models import *

from django import forms

class SubmissionForm(forms.Form):
	language =  forms.ModelChoiceField(Language.objects.all())
	userCode = forms.FileField()

	def __init__(self, *args, **kwargs):
		problem = kwargs.pop('problem', None)
	        super(SubmissionForm, self).__init__(*args, **kwargs)
		if problem:
			self.fields['language'].queryset= problem.languages


	
