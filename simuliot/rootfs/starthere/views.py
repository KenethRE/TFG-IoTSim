from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PlanoUpload
from .models import Plano
import os
# Create your views here.

def start(request):
	return render(request, 'start.html')

def upload_plano(request):
	if request.method == 'POST':
		form = PlanoUpload(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('display_plano')
	else:
		planos = Plano.objects.all()
		for plano in planos:
			plano.delete()
			if os.path.exists(plano.Subir_Plano.path):
				os.remove(plano.Subir_Plano.path)
		form = PlanoUpload()
	return render(request, 'upload_plano.html', {'form': form})


def success(request):
	return HttpResponse('successfully uploaded')

def display_plano(request):
	if request.method == 'GET':
		# getting all the objects of planos.
		LastPlano = Plano.objects.last()
		if LastPlano is not None:
			return render(request, 'display_images.html', {'plano': LastPlano})
		else:
			return render(request, 'error_no_maps_available.html', status=404)