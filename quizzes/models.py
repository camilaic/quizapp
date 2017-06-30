from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    # to define the singular and plural for model when displaying in the admin?
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    question = models.CharField(max_length=200)  # the row with the question
    quiz = models.ForeignKey(Quiz)  # point to the Quiz, creating a relationship many-to-one

    def __str__(self):
        return self.question


class Choice(models.Model):
    # foreignkey: each Choice is related to a single question on the quiz
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)  # choice text
    is_correct = models.BooleanField(default=False)
    # is_correct = models.BooleanField(db_column='answer', default=False)
    # db_column: allows to make the migration later

    def __str__(self):
        return self.choice_text


class UserAnswer(models.Model):
    user_answer = models.ForeignKey(Choice)
    user = models.ForeignKey(User)
    quiz_attempt_id = models.IntegerField(null=False, default=0)
    # max_length is defined as 36 because the uuid length is 36

    class Meta:
        unique_together = ('user_answer', 'user', 'quiz_attempt_id')
