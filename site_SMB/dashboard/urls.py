from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
        path('', views.dashboard, name='dashboard'),
        path('runGraph/', views.runGraph, name='runGraph'),
        ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

