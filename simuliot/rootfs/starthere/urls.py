from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_plano, success, display_session, start, create_session, terminate_session

urlpatterns = [
	path('', start, name='start'),
	path('upload_map', upload_plano, name='upload_map'),
	path('success', success, name='success'),
	path('display_session', display_session, name = 'display_session'),
	path('create_session', create_session, name = 'create_session'),
	path('terminate_session', terminate_session, name = 'terminate_session'),
	path('start_session', start, name = 'start_session'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,
						document_root=settings.MEDIA_ROOT)