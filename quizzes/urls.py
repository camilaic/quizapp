from django.conf.urls import url
from . import views

app_name = 'quizzes'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # name: used to identify the view
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<quiz_id>[0-9]+)/answer/$', views.answer, name='answer'),
]