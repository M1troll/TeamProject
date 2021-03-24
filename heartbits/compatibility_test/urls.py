from django.urls import path, re_path
from . import views


urlpatterns = [
    path('test/<int:pk>', views.test_detail, name='test'),
    path('answer/', views.test_detail, name='answer'),
]