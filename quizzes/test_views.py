from django.test import TestCase
from django.urls import reverse
from .models import Quiz, Question, Choice, User, UserAnswer


def create_quiz(choice_test, choice_status):
    quiz = Quiz.objects.create(name='QuizTest')
    question = Question.objects.create(question='Is it raining?', quiz=quiz)
    choice = Choice.objects.create(question=question, choice_text=choice_test, is_correct=choice_status)
    # user = User.objects.create(username='camila', email='admin@mail.com', is_staff=True)
    # UserAnswer.objects.create(user_answer=choice, user=user, quiz_attempt_id=1)

    return choice


class TestIndexView(TestCase):
    def test_index_list_view(self):
        index_url = reverse('quizzes:index')
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 200)

    def test_no_questions(self):
        # if no questions exist, display message
        response = self.client.get(reverse('quizzes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No quizzes are available.")
        # verifies that quiz_list is empty
        self.assertQuerysetEqual(response.context['quiz_list'], [])

    # verifies if the created quiz appears in the list: quiz_list
    def test_questions(self):
        create_quiz(choice_test='Yes', choice_status=True)
        response = self.client.get(reverse('quizzes:index'))
        self.assertQuerysetEqual(
            response.context['quiz_list'], ['<Quiz: QuizTest>'])


class TestDetailView(TestCase):
    # verifying if the created choice is returned
    def test_choice(self):
        choice = create_quiz(choice_test='Always', choice_status=True)
        url = reverse('quizzes:detail', args=(choice.id, ))
        response = self.client.get(url)
        self.assertContains(response, choice.choice_text)

    # verifying if the created choice points to the correct question
    def test_question(self):
        choice = create_quiz(choice_test='No', choice_status=True)
        url = reverse('quizzes:detail', args=(choice.question.quiz_id,))
        response = self.client.get(url)
        self.assertContains(response, choice.question)


# class TestResultView(TestCase):
    # testing if only the corrected choice is returned
    # def test_correct_choice(self):
    #     choice_1 = create_quiz(choice_test='Yes', choice_status=True)
    #     choice_2 = create_quiz(choice_test='Never', choice_status=False)

