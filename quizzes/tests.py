from django.test import TestCase
from .models import Quiz, Question, UserAnswer


# Create your tests here.
class QuestionModelTestCase(TestCase):
    def setUp(self):
        Quiz.objects.create(name='QuizTest')

    def test_question_question(self):
        obj = Quiz.objects.get(name='QuizTest')
        self.assertEqual(obj.name, 'QuizTest')

        





