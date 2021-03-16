from django.urls import path, include
from accounts import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
]