from django.test import TestCase
from .models import Quiz, Question, Choice, User, UserAnswer


# Create your tests here.
class QuizModelTestCase(TestCase):
    def setUp(self):
        Quiz.objects.create(name='QuizTest')

    def test_quiz_name(self):
        obj = Quiz.objects.get(name='QuizTest')
        self.assertEqual(obj.name, 'QuizTest')


class QuestionToQuizModelTestCase(TestCase):
    def setUp(self):
        quiz_name = Quiz.objects.create(name='QuizTest')
        Question.objects.create(question='How are you', quiz=quiz_name)

    # testing that the question point to the correct quiz
    def test_question_point_to_quiz(self):
        obj = Question.objects.get(question='How are you')
        self.assertEqual(obj.quiz.name, 'QuizTest')


class ChoiceModelTestCase(TestCase):
    def setUp(self):
        quiz = Quiz.objects.create(name='QuizTest')
        question = Question.objects.create(question='How are you', quiz=quiz)
        Choice.objects.create(question=question, choice_text='Good', is_correct=False)
        Choice.objects.create(question=question, choice_text='Bad', is_correct=True)

    # testing if the choice points to the correct boolean value
    def test_choice(self):
        obj = Choice.objects.get(choice_text='Good')
        self.assertEqual(obj.is_correct, False)

    # testing if the query return the correct number of items
    def test_query(self):
        query = Choice.objects.filter(choice_text='Bad')
        self.assertEqual(query.count(), 1)


class UserAnswerTestCase(TestCase):
    def setUp(self):
        quiz = Quiz.objects.create(name='QuizTest')
        question = Question.objects.create(question='How are you', quiz=quiz)
        choice = Choice.objects.create(question=question, choice_text='Bad', is_correct=True)
        user = User.objects.create(username='camila', email='admin@mail.com', is_staff=True)
        # user_2 = User.objects.create(username='test', email='test @mail.com', is_staff=True)
        UserAnswer.objects.create(user_answer=choice, user=user, quiz_attempt_id=1)
        # user2 = UserAnswer.objects.create(user_answer=choice, user=user_2, quiz_attempt_id=1)

    # testing if the user points to the user choice and asserting that is equal to 'Bad'
    def test_user_answer(self):
        obj = UserAnswer.objects.get(user__username='camila')
        self.assertEqual(obj.user_answer.choice_text, 'Bad')

    # test for uniqueness - unique_together = ('user_answer', 'user', 'quiz_attempt_id')
    # def test_uniqueness(self):




