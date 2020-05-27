from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', views.listFiles, name='dashboard'),
        path('runGraph', views.runGraph, name='runGraph')
        ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
