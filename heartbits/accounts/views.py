from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .forms import MyUserCreationForm, MyUserChangeForm, LoginUserForm
from heartbits_app.models import User
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.


class SignUp(generic.CreateView):
    model = User
    form_class = MyUserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/register.html'


class Login(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class Logout(LogoutView):
    next_page = 'index'
    template_name = 'accounts/logout.html'


def login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                return redirect('index', {'user': user})
            else:
                return HttpResponseRedirect('index')
        return HttpResponseRedirect('index')
    else:
        form = LoginUserForm()
        return render(request, 'accounts/login.html', context={'form': form})


# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST, request.FILES)
#         if form.is_valid():
#             if form.cleaned_data['password'] == form.cleaned_data['password2']:
#                 userdata = form.save(commit=False)
#                 userdata.password = make_password(form.cleaned_data['password2'])
#                 userdata.save()
#                 form.clean()
#         return render(request, 'index')
#     if request.method == 'GET':
#         form = RegisterUserForm()
#         return render(request, 'accounts/register.html', context={'reg_form': form})
#
#
