from django.shortcuts import render, get_object_or_404, redirect
from heartbits_app.models import Question, Test, Answer, User
import json
# Create your views here.
answers = {}


def test_detail(request, pk=1):
    test = Test.objects.get(user=request.user.pk)
    current_question = test.test_questions.get(pk=pk)
    if request.method == 'POST':
        if 'answer' in request.POST:
            data = request.POST['answer']
            next_question = Question.objects.filter(id__gt=current_question.id).order_by('id').first()
            if next_question is not None:
                answers[current_question.id.__str__()] = Answer.objects.get(pk=data).weight
                return redirect('/test/%s' % next_question.pk)
            test.result = answers
            test.save()
            User.make_recommendation(request.user, 5)
            return render(request, 'comp_test/answer.html')
        else:
            return redirect('/test/%s' % current_question.pk)
    else:
        if request.user.is_authenticated:
            question = get_object_or_404(Question, pk=pk)
            return render(request, 'comp_test/comp_test.html', context={'question': question})
        return redirect('login')
