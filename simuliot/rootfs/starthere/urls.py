from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_plano, success, display_plano, start

urlpatterns = [
	path('', start, name='start'),
	path('upload_plano', upload_plano, name='upload_plano'),
	path('success', success, name='success'),
	path('display_plano', display_plano, name = 'display_plano'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,
						document_root=settings.MEDIA_ROOT)