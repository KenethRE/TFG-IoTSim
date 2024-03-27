from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
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
							new_device = Devices.objects.create_session_device(deviceinfo['id'], deviceinfo['name'], deviceinfo['type'], location['location'])
							session_devices.append(new_device.printDevice())
			
			req = urllib.request.Request('http://127.0.0.1:8088/devices', json.dumps(session_devices).encode(), {'Content-Type': 'application/json'}, method='POST')
			response = urllib.request.urlopen(req)
			if response.status == 400:
				return HttpResponse('Please wait for previous session to be stored. Saved button pressed multiple times.', status=400)
			## trigger save session in backend
			req = urllib.request.urlopen('http://127.0.0.1:8088/store-session')
			if req.status == 201:
				return HttpResponseRedirect('/display_session')
			else:
				return HttpResponse('Error storing session', status=500)
		except Exception as e:
			print(e)
		return HttpResponse('successfully uploaded')

def display_session(request):
	if request.method == 'GET':
		devices = []
		req = urllib.request.urlopen('http://127.0.0.1:8088/start-session')
		if req.status == 200:
			devices_back = json.loads(urllib.request.urlopen('http://127.0.0.1:8088/retrieve-session').read())

			for device in devices_back:
				new_device = Devices.objects.create_session_device_value(device['id'], device['name'], device['type'], device['location'], device['value'])
				devices.append(new_device)
			return render(request, 'display_session.html', {'devices': devices})
		else:
			return HttpResponse('Error starting session', status=500)

def terminate_session(request):
	if request.method == 'GET':
		req = urllib.request.urlopen('http://127.0.0.1:8088/kill-session')
		if req.status == 200:
			Devices.objects.all().delete()
			return HttpResponseRedirect('/start')
		else:
			return HttpResponse('Error terminating session', status=500)