# forms.py
from django import forms
from .models import Plano


class MapUpload(forms.ModelForm):
	class Meta:
		model = Plano
		fields = ['Upload_Map']
