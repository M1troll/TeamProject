from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from heartbits_app.models import Question, Test, Answer, User
import json
# Create your views here.
answers = {}


@login_required(login_url='login')
def test_render(request):
    test = Test.objects.get(user_id=request.user.pk)
    if not test.result or len(test.result) != len(test.test_questions.all()):
        if request.method == 'GET':
            question = Question.objects.first()
            return render(request, 'comp_test/comp_test.html', context={'question': question})
    return redirect('/%s/matches' % User.objects.get(pk=request.user.pk).user_url)


@login_required(login_url='login')
def test_ajax(request, pk):
    if request.method == 'POST':
        test = Test.objects.get(user=request.user.pk)
        if not test.result:
            test.result = {}
        current_question = test.test_questions.get(pk=pk)
        if 'answer' in request.POST:
            data = request.POST['answer']
            next_question = Question.objects.filter(id__gt=current_question.id).order_by('id').first()
            if next_question is not None:
                test.result[current_question.id.__str__()] = Answer.objects.get(pk=data).weight
                test.save()
                html_response = '<p class="card-header text-center">' + next_question.title \
                                + '</p>' + '<p class="card-title">' + next_question.description + '</p>' + \
                                '<div class="card-body"><form id="test-form" data-question-id="' + str(next_question.id) + '">' + \
                                '<input type="hidden" name="csrfmiddlewaretoken" value="' + str(
                    csrf(request)['csrf_token']) \
                                + '">'
                for answer in next_question.answer_set.all():
                    html_response += '<p><input class="form-check-input" type="radio" name="answer" value="' + \
                                     str(answer.pk) + '">' + answer.answer + '</p>'
                html_response += '<input type="submit" value="OK"></form></div>'
                response = {
                    'question_html': html_response
                }
                return JsonResponse(response)
            test.save()
            response = {
                'redirect_url': '/%s/matches' % User.objects.get(pk=request.user.pk).user_url
            }
            return JsonResponse(response)
    else:
        question = Question.objects.filter(id__gt=pk).order_by('id').first()
        html_response = '<p>' + question.title + '</p>' + '<p>' + question.description + '</p>' + \
                        '<form id="test-form" data-question-id="' + str(question.id) + '">' + \
                        '<input type="hidden" name="csrfmiddlewaretoken" value="' + str(csrf(request)['csrf_token']) \
                        + '">'
        for answer in question.answer_set.all():
            html_response += '<input type="radio" name="answer" value="' + \
                             str(answer.pk) + '">' + answer.answer + '<br>'
        html_response += '<input type="submit" value="OK"></form>'
        response = {
            'question_html': html_response
        }
        return JsonResponse(response)
