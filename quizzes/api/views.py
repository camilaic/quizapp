from django.db.models import Max
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quizzes import models
from . import serializers


class UserAttempt:

    def __init__(self):
        self.quiz_id = 0
        self.user = "Anonymous"
        self.current_attempt_id = 0

    def generate_user_attempt_id(self, data):
        self.quiz_id = data['user_answer'].question.quiz_id
        self.user = data['user']

        # global quiz_id, user, current_attempt_id
        previous_choices = models.UserAnswer.objects.filter(
            user=self.user,
            user_answer__in=models.Choice.objects.filter(question__quiz_id=self.quiz_id))

        previous_attempt_id = previous_choices.aggregate(Max('quiz_attempt_id'))['quiz_attempt_id__max'] or 0
        self.current_attempt_id = previous_attempt_id + 1

        return self.current_attempt_id


class UserResult:

    def __init__(self, user_attempt):
        self.quiz_id = user_attempt.quiz_id
        self.user = user_attempt.user
        self.current_attempt_id = user_attempt.current_attempt_id

    # only the user score
    def user_score(self):

        correct_choices = self.correct_choice
        current_user_answers = self.current_user_answers
        correct_guesses = 0

        # iterating through correct_choice and current_user_answers and checking if the values matches
        for choice, current_user_answer in zip(correct_choices.order_by('question_id'),
                                               current_user_answers.order_by('user_answer__question_id')):
            if choice.choice_text == current_user_answer.user_answer.choice_text:
                # if they match, correct_guesses is incremented
                correct_guesses += 1

        return correct_guesses

    @property
    def correct_choice(self):
        # getting the correct choice marked as is_correct=True
        correct_choice = models.Choice.objects.filter(question__quiz_id=self.quiz_id,
                                                      is_correct=True
                                                      ).select_related('question__quiz')

        return correct_choice

    @property
    def current_user_answers(self):
        current_user_answers = models.UserAnswer.objects.filter(user=self.user,
                                                                user_answer__question__quiz_id=self.quiz_id,
                                                                quiz_attempt_id=self.current_attempt_id
                                                                ).select_related('user_answer__question')

        return current_user_answers

    # iterate through the returned list from current_user_answer and save them into a dictionary
    def question_and_user_answers_to_dict(self):
        current_user_answers = self.current_user_answers
        answer_and_questions_dict = {}

        # getting the current question and user answer
        for current_user_answer in current_user_answers:
            question = current_user_answer.user_answer.question.question
            answers = current_user_answer.user_answer.choice_text

            # saving into a dictionary, key is the question
            answer_and_questions_dict[question] = answers

        return answer_and_questions_dict

    # iterate through the returned list from correct_choice property and save them into a dictionary
    def correct_choice_to_dict(self):
        choices_and_questions_dict = {}
        correct_choice = self.correct_choice

        # getting the correct choice marked as is_correct=True
        for current_choice in correct_choice:
            question = current_choice.question.question
            choice = current_choice.choice_text

            # saving into the dictionary, question-text as a key
            choices_and_questions_dict[question] = choice

        return choices_and_questions_dict


# ResultsViewSet is specific
class UserAnswersViewSet(ModelViewSet):

    user_attempt = UserAttempt()

    # getting all the objects from UserAnswer model
    queryset = models.UserAnswer.objects.all()
    # getting the UserAnswerSerializer class from serializers.py
    serializer_class = serializers.UserAnswerSerializer
    # permission class will deny permission to any unauthenticated user. API only accessible to registered users.
    permission_classes = (IsAuthenticated,)

    # from mixins.py - overwriting create and perform_create of CreateModelMixin
    # creating and saving a new model instance
    def create(self, request, *args, **kwargs):
        # many=True: accept multiple objects
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user_result = UserResult(self.user_attempt)

        data = {
            "score_correct": user_result.user_score(),
            "user_answers": user_result.question_and_user_answers_to_dict(),
            "correct_choice": user_result.correct_choice_to_dict()
        }

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # looping through the serializer to add the user username
        for data in serializer.validated_data:
            data['user'] = self.request.user
            data['quiz_attempt_id'] = self.user_attempt.generate_user_attempt_id(data)
        super().perform_create(serializer)
