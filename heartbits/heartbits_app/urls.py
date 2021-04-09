from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    re_path(r'\w+\/matches', views.matches, name='matches'),
]