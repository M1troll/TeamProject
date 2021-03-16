from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from .forms import RegisterUserForm, LoginUserForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                userdata = form.save(commit=False)
                userdata.password = make_password(form.cleaned_data['password2'])
                userdata.save()
                form.clean()
                return HttpResponseRedirect('index/index.html')
    if request.method == 'GET':
        form = RegisterUserForm()
        return render(request, 'accounts/register.html', context={'reg_form': form})


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
