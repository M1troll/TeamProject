from django.urls import path, include
from accounts import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register/', views.SignUp.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('<slug:slug>/', login_required(login_url='login')(views.UserUpdateView.as_view()), name='user_update')
]