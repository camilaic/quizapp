from django.conf.urls import include, url
from django.contrib import admin
from quizzes import views

urlpatterns = [
    # url(r'^quiz/(?P<quiz_id>[0-9]+)/$', views.quiz, name='quiz'),
    url(r'^quizzes/', include('quizzes.urls')),
    url(r'^admin/', admin.site.urls),
]
