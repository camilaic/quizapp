from quizzes.api.views import UserAnswersViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register('^user_answers', UserAnswersViewSet)
# it will generate:
# ^user_answers/$ : api:useranswer-list
#  ^user_answers/{pk}/ : api:useranswer-detail

urlpatterns = router.urls
