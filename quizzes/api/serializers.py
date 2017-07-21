from rest_framework.serializers import ModelSerializer

from .. import models


class UserAnswerSerializer(ModelSerializer):
    class Meta:
        model = models.UserAnswer
        fields = ('user_answer', )
