from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User, UserRating

# Create your views here.


def main(request):
    user = request.user
    return render(request, 'main/main.html', context={'user': user})


@login_required(login_url='login')
def matches(request):
    current_user = User.objects.get(pk=request.user.pk)
    matches = current_user.make_recommendation(current_user)
    recommended_users = []
    for match in matches:
        user = User.objects.get(pk=match[0])
        if user.calculate_age() <= current_user.partner_max_age and \
                (user.sex == current_user.partner_sex or current_user.partner_sex == 'ND'):
            recommended_users.append(user)
    return render(request, 'matches/matches.html', {'recommended_users': recommended_users})


def developers(request):
    return render(request, 'developers/developers.html')


@login_required(login_url='login')
def user_like_ajax(request):
    if request.method == 'POST':
        pk = request.POST['pk'][0]
        user = User.objects.get(pk=pk)
        like, created = UserRating.objects.get_or_create(user=user, id_user_liked=request.user)
        if created:
            response = {
                'success': True,
                'action': 'create',
                'user_likes': user.get_user_likes(),
            }
            return JsonResponse(response)
        like.delete()
        response = {
            'success': True,
            'action': 'delete',
            'user_likes': user.get_user_likes(),
        }
        return JsonResponse(response)




