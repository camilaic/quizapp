from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Choice, Quiz


class IndexView(generic.ListView):
    template_name = 'quizzes/index.html'
    context_object_name = 'quiz_list'

    def get_queryset(self):
        return Quiz.objects.order_by('?')

# def index(request):
#     # order randomly
#     quiz_list = Quiz.objects.order_by('?')
#     context = {
#         'quiz_list': quiz_list,
#     }
#
#     # quiz = get_object_or_404(models.Quiz, pk=quiz_id)
#     return render(request, 'quizzes/index.html', context)


class DetailView(generic.DetailView):
    model = Quiz
    template_name = 'quizzes/detail.html'
    context_object_name = 'quiz'

# def detail(request, quiz_id):
#         question = get_object_or_404(Quiz, pk=quiz_id)
#         return render(request, 'quizzes/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Quiz
    template_name = 'quizzes/results.html'


# def results(request, quiz_id):
#     question = get_object_or_404(Quiz, pk=quiz_id)
#     return render(request, 'quizzes/results.html', {'question': question})
#     # response = "Results of quiz %s."
#     # return HttpResponse(response, quiz_id)


def answer(request, quiz_id):
    question = get_object_or_404(Quiz, pk=quiz_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # redisplay the question
        return render(request, 'quizzes/detail.html', {
            'question': question,
            'error_message': "Select an answer.",
        })
    else:
        selected_choice.answer += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('quizzes:results', args=(quiz_id,)))
