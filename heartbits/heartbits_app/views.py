from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import User

# Create your views here.


def main(request):
    user = request.user
    return render(request, 'main/main.html', context={'user': user})


@login_required(login_url='login')
def matches(request):
    current_user = User.objects.get(pk=request.user.pk)
    matches = current_user.make_recommendation(current_user)
    print(matches)
    recommended_users = []
    for match in matches:
        user = User.objects.get(pk=match[0])
        print(user)
        if user.calculate_age() <= current_user.partner_max_age and \
                (user.sex == current_user.partner_sex or current_user.partner_sex == 'ND'):
            recommended_users.append(user)
    print(recommended_users)
    return render(request, 'matches/matches.html', {'recommended_users': recommended_users})




