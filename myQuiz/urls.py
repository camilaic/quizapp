from django.conf.urls import include, url
from django.contrib import admin
from quizzes.api.urls import urlpatterns


urlpatterns = [
    # url(r'^quiz/(?P<quiz_id>[0-9]+)/$', views.quiz, name='quiz'),
    url(r'^quizzes/', include('quizzes.urls')),
    url(r'^api/', include(urlpatterns, namespace='api')),
    url(r'^admin/', admin.site.urls),
]
