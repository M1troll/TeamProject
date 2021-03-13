from django.shortcuts import render
from .forms import RegisterUserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password

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
        return render(request, 'register/register.html', context={'reg_form': form})
