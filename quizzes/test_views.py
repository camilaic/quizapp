from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Choice, Question, Quiz, UserAnswer
from .views import answer


# testing index view which displays the list of quizzes
class TestIndexView(TestCase):
    def setUp(self):
        quiz = Quiz.objects.create(name='QuizTest')
        Question.objects.create(question='Is it raining?', quiz=quiz)

    # verifying if it returns the page
    def test_index_list_view(self):
        index_url = reverse('quizzes:index')
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 200)

    # def test_no_questions(self):
    #     # if no questions exist, display message
    #     response = self.client.get(reverse('quizzes:index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "No quizzes are available.")
    #     # verifying that the quiz_list is empty
    #     self.assertQuerysetEqual(response.context['quiz_list'], [])

    # verifying if the quiz appears in the list: quiz_list
    def test_questions(self):
        response = self.client.get(reverse('quizzes:index'))
        # self.assertQuerysetEqual(
        #     response.context['quiz_list'], ['<Quiz: QuizTest>'])
        obj = Quiz.objects.get(name='QuizTest')
        query = response.context['quiz_list']
        self.assertEqual(query[0], obj)


# testing the detail view which displays the questions and choices
class TestDetailView(TestCase):
    def setUp(self):
        quiz = Quiz.objects.create(name='QuizTest')
        question = Question.objects.create(question='Is it raining?', quiz=quiz)
        Choice.objects.create(question=question, choice_text='Yes', is_correct=True)

    # verifying if choice is returned
    def test_choice(self):
        choice = Choice.objects.get(choice_text='Yes')
        # args passing the pk
        url = reverse('quizzes:detail', args=(choice.id,))
        response = self.client.get(url)
        self.assertContains(response, choice.choice_text)

    # verifying if the choice points to the correct question
    def test_question(self):
        choice = Choice.objects.get(choice_text='Yes')
        url = reverse('quizzes:detail', args=(choice.question.quiz_id,))
        response = self.client.get(url)
        self.assertContains(response, choice.question)


# testing the result view which displays how many questions were answered correctly
class TestResultView(TestCase):
    def setUp(self):
        quiz = Quiz.objects.create(name='QuizTest')
        question = Question.objects.create(question='Is it raining?', quiz=quiz)
        correct_choice = Choice.objects.create(question=question, choice_text='Yes', is_correct=True)
        Choice.objects.create(question=question, choice_text='No', is_correct=False)

        user = User.objects.create_user(username='camila', password='test123')
        # user answer to test
        UserAnswer.objects.create(user_answer=correct_choice, user=user, quiz_attempt_id=2)

    # return correct count for the user answers that are correct
    def test_return_correct_choice(self):
        choice = Choice.objects.get(choice_text='Yes')
        url = reverse('quizzes:results', args=(choice.question.quiz_id,))

        # to prevent 'AnonymousUser'
        client = Client()
        client.login(username='camila', password='test123')

        response = client.get(url)

        # get the number of user correct_guesses
        query = response.context['correct_guesses']

        # as the user answer is correct, correct_guesses should be equal to one
        self.assertEqual(query, 1)

    def test_return_user_answer(self):
        user_answer = UserAnswer.objects.get(user_answer__choice_text='Yes')
        url = reverse('quizzes:results', args=(user_answer.user_answer.question.quiz_id,))

        # to prevent 'AnonymousUser'
        client = Client()
        client.login(username='camila', password='test123')

        response = client.get(url)

        # verifying if the url contains the user answer=Yes
        self.assertContains(response, 'Yes')
