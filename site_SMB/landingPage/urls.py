from django.urls import path
from . import views

urlpatterns = [
        path('', views.englishRedirect, name='redirect'),
        path('en', views.landingPage, name='landingPageEn'),
        path('zh-cn', views.landingPageCN, name='landingPageCN'),
]

