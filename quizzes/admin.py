from django.contrib import admin
from .models import Choice, Quiz, Question, UserAnswer, User


# displays in a table format: TabularInLine
class ChoiceInLine(admin.TabularInline):
    model = Choice
    # create two extras slots for choices in questions
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    # reordering the page in admin
    fields = ['quiz', 'question']
    search_fields = ['question']
    # referencing choices inside questions
    inlines = [ChoiceInLine]


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz_attempt_id', 'user_answer')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz)
admin.site.register(UserAnswer, UserAnswerAdmin)

