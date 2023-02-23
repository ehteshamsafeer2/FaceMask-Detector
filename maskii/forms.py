# forms.py
from django import forms
from .models import *


class DetectForm(forms.ModelForm):
	class Meta:
		model = FileUpload
		fields = ['img']
