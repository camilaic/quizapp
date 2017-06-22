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
    question = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz)

    def __str__(self):
        return self.question


class Choice(models.Model):
    # foreignkey: each Choice is related to a single question on the quiz
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    # ??
    answer = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

#
# class User(models.Model):
#     user = models.CharField(max_length=100)


class UserAnswer(models.Model):
    user_answer = models.ForeignKey(Choice)
    user = models.ForeignKey(User)
