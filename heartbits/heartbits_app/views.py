from django.shortcuts import render
from .forms import LoginUserForm
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):
    return render(request, 'index/index.html')


def log_in(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)


