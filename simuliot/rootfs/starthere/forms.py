# forms.py
from django import forms
from .models import Plano, Devices


class MapUpload(forms.ModelForm):
	class Meta:
		model = Plano
		fields = ['Upload_Map']

class UpdateDeviceValue(forms.ModelForm):
	class Meta:
		model = Devices
		fields = ['Value']