from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Choice, Quiz, UserAnswer


# displays list of quizzes
class IndexView(generic.ListView):
    template_name = 'quizzes/index.html'
    context_object_name = 'quiz_list'

    def get_queryset(self):
        return Quiz.objects.order_by('name')


# displays questions
class DetailView(generic.DetailView):
    model = Quiz
    template_name = 'quizzes/detail.html'
    context_object_name = 'quiz'  # context


# displays the results (correct and user answer, and overall score)

class ResultsView(generic.DetailView):
    model = Quiz
    template_name = 'quizzes/results.html'

    def get_context_data(self, **kwargs):
        correct_guesses = 0
        context = super(ResultsView, self).get_context_data(**kwargs)

        # get the correct choice marked as is_correct=True
        correct_choice = Choice.objects.filter(question__quiz=kwargs['object'], is_correct=True)

        # get all the user attempts: get the result of filtering user_answer in Choice, which has the returned
        # result of the filter question in quiz that has 'key' 'object' ({'object': <Quiz: quiz2>})
        all_attempt_answers = UserAnswer.objects.filter(
            user=self.request.user, user_answer__in=Choice.objects.filter(
                question__quiz=kwargs['object']))
        all_attempt_answers.order_by('quiz_attempt_id')

        # get the maximum value where the id is equal to quiz_attempt_id and return the id of the quiz_attempt_id
        # that has the highest value
        latest_attempt_id = all_attempt_answers.aggregate(Max('quiz_attempt_id'))['quiz_attempt_id__max']

        # send the last attempt to the template under the user_answer variable
        attempt_answer = all_attempt_answers.filter(quiz_attempt_id=latest_attempt_id)

        # iterating through correct_choice and attempt_answer and checking if the values matched
        # order_by to order the answers and questions. Without it, the result is wrong
        # if they match, correct_guesses is incremented
        for choice, user_answer in zip(correct_choice.order_by('question_id'),
                                       attempt_answer.order_by('user_answer__question_id')):
            if choice.choice_text == user_answer.user_answer.choice_text:
                correct_guesses += 1

        context['user_answer'] = attempt_answer
        context['correct_guesses'] = correct_guesses

        return context


# save the user answer and show the next question
def answer(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user

    previous_choices = UserAnswer.objects.filter(user=user, user_answer__in=Choice.objects.filter(question__quiz=quiz))
    previous_attempt_id = previous_choices.aggregate(Max('quiz_attempt_id'))['quiz_attempt_id__max'] or 0
    current_attempt_id = previous_attempt_id+1

    # calling the function, passing the dictionary from the form
    question_id_to_chosen_answers_ids = get_questions_and_answer(request.POST)

    try:
        # get selected_questions that matches the key
        selected_questions = quiz.question_set.filter(pk__in=question_id_to_chosen_answers_ids.keys())

        # iterating through the selected_question to get the selected choice and get the question pk
        for question in selected_questions:
            selected_choices = question.choice_set.filter(pk__in=question_id_to_chosen_answers_ids[question.pk])

            # iterating through selected_choices to get the user's choice and saving into the table UserAnswer
            # the choice can be linked back to the question
            for choice in selected_choices:
                UserAnswer(user_answer=choice, user=request.user, quiz_attempt_id=current_attempt_id).save()

    except(KeyError, Choice.DoesNotExist):
        # redisplay the questions if the choice was empty
        # redirect to the same template detail.html, thus, it is necessary to send the context = quiz
        return render(request, 'quizzes/detail.html', {
            # before I was passing the wrong context: 'question'
            'quiz': quiz,
            'error_message': "Select an answer.",
            })

    return HttpResponseRedirect(reverse('quizzes:results', args=(quiz_id,)))


# it will get the keys and values from the dictionary from the form, handling it and saving to a temp_dict
def get_questions_and_answer(post_data):
    temp_dict = {}

    # before, it was post_data.items()
    for key, value in post_data.lists():
        # matches the key
        if key.startswith('question'):
            # remove the 'question' from the key
            question_id = int(key[8:])

            # adding the key and value (for example: [2:8])
            temp_dict[question_id] = value

    return temp_dict
