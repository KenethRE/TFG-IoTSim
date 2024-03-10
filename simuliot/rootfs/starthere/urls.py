from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_plano, success, display_map, start

urlpatterns = [
	path('', start, name='start'),
	path('upload_map', upload_plano, name='upload_map'),
	path('success', success, name='success'),
	path('display_map', display_map, name = 'display_map'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,
						document_root=settings.MEDIA_ROOT)