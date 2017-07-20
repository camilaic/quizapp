from quizzes.api.views import ResultsViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register('^results', ResultsViewSet)
# it will generate:
# ^results/$ : api:useranswer-list
#  ^results/{pk}/ : api:useranswer-detail

urlpatterns = router.urls
