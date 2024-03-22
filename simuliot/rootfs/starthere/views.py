from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core import serializers
from .forms import MapUpload
from .models import Plano, Devices
import os
import json
import urllib.request
# Create your views here.

def start(request):
	planos = Plano.objects.count()
	return render(request, 'start.html', {'planos': planos})

def upload_plano(request):
	if request.method == 'POST':
		form = MapUpload(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('display_map')
	else:
		planos = Plano.objects.all()
		devices = Devices.objects.all()
		for plano in planos:
			plano.delete()
			if os.path.exists(plano.Upload_Map.path):
				os.remove(plano.Upload_Map.path)
		for device in devices:
			device.delete()
		form = MapUpload()
	return render(request, 'upload_map.html', {'form': form})


def success(request):
	return HttpResponse('successfully uploaded')

def create_session(request):
	if request.method == 'GET':
		devices = []
		# We get all devices from backend
		try:
			devices_back = json.loads(urllib.request.urlopen('http://127.0.0.1:8088/all-devices').read())
			for device in devices_back:
				new_device = Devices.objects.create_device(device['id'], device['type'], device['name'], device['manufacturer'])
				devices.append(new_device)
		except Exception as e:
			print(e)
			devices = []
		return render(request, 'create_session.html', {'devices': devices})
	elif request.method == 'POST':
		#if devices.count('DeviceID') == 0:
		#	return HttpResponse('No devices available. Invalid method used', status=500)
		try:
			# We get all devices from backend
			devices_back = json.loads(urllib.request.urlopen('http://127.0.0.1:8088/all-devices').read())
			session_devices = []
			# We get devices from session from request
			locations = json.loads(request.body)
			for deviceinfo in devices_back:
				for location in locations:
					for device in location['devices']:
						if deviceinfo['id'] == device:
							new_device = Devices.objects.create_session_device(deviceinfo['id'], deviceinfo['type'], location['location'])
							print(new_device.printDevice())
							session_devices.append(new_device)
		except Exception as e:
			print(e)
		return HttpResponse('successfully uploaded')

def display_map(request):
	if request.method == 'GET':
		# We get the last Plano uploaded
		LastPlano = Plano.objects.last()
		devices = []
		if LastPlano is not None:
			# We get all devices from backend
			try:
				devices_back = json.loads(urllib.request.urlopen('http://127.0.0.1:8088/all-devices').read())
				for device in devices_back:
					new_device = Devices.objects.create_device(device['id'], device['type'], device['name'], device['manufacturer'])
					devices.append(new_device)
					new_device.save()
			except Exception as e:
				print(e)
				devices = []
			return render(request, 'display_map.html', {'devices': devices, 'map': LastPlano})
		else:
			return render(request, 'error_no_maps_available.html', status=404)
	else:
		return HttpResponse(status=403)