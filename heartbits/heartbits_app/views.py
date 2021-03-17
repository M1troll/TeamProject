from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):
    user = request.user
    return render(request, 'index/index.html', context={'user': user})


