from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('developers/', views.developers, name='developers'),
    re_path(r'\w+\/matches', views.matches, name='matches'),
]