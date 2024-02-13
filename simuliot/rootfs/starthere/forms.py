# forms.py
from django import forms
from .models import Plano


class PlanoUpload(forms.ModelForm):
	class Meta:
		model = Plano
		fields = ['Nombre_Imagen', 'Subir_Plano']
