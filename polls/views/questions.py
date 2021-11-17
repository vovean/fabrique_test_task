from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from polls.models import Question
from polls.serializers import QuestionAdminSerializer


class QuestionViewSet(mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionAdminSerializer
    queryset = Question.objects.all()
