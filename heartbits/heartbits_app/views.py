from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.


def main(request):
    user = request.user
    return render(request, 'main/main.html', context={'user': user})


