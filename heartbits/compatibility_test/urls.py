from django.urls import path, re_path
from . import views


urlpatterns = [
    path('test/', views.test_render, name='test-render'),
    path('test-ajax-<int:pk>/', views.test_ajax, name='test-ajax'),
]