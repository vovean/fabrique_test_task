from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Subquery
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from polls.exceptions import InvalidUserIDException, UserIDNotProvidedException, AnswersNotFoundException, \
    NotEnoughAnswersException, InvalidAnswerFormatException, IdInCreateRequestException
from polls.models import Poll, Answer, Question
from polls.permissions import IsAdminOrReadOnly
from polls.serializers import PollCommonSerializer, PollDetailAdminSerializer, PollDetailSerializer, \
    QuestionUserSerializer, QuestionWithAnswerSerializer

User = get_user_model()


class PollViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Poll.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'update', 'partial_update'):
            return PollCommonSerializer
        elif self.action in ('retrieve', 'create'):
            # check that self.request is present (for generating OpenAPI docs)
            if self.request and self.request.user.is_staff:
                return PollDetailAdminSerializer
            return PollDetailSerializer
        # default serializer for OpenAPI docs
        return PollCommonSerializer

    def get_answering_user(self, request: Request):
        if not request.user.is_anonymous:
            return request.user.id
        if 'user_id' in request.data:
            user_id = str(request.data['user_id'])
            if not user_id.isnumeric():
                raise InvalidUserIDException
            return int(user_id)
        raise UserIDNotProvidedException

    @action(detail=True, methods=('post',), permission_classes=[])
    def answer(self, request: Request, pk: int):
        poll = get_object_or_404(Poll, pk=pk)
        if 'answers' not in request.data:
            raise AnswersNotFoundException
        answers = request.data['answers']
        if len(answers) != poll.questions.count():
            raise NotEnoughAnswersException
        user_id = self.get_answering_user(request)
        for question, answer in zip(poll.questions.all(), answers):
            if not isinstance(answer, (str, int)):
                raise InvalidAnswerFormatException
            Answer.objects.create(question=question, user_id=user_id, text=str(answer))
        return Response(status=HTTP_204_NO_CONTENT)

    def validate_and_enrich_question_data(self, poll: Poll, data: dict):
        # this may cause IntegrityError if not checked
        if 'id' in data:
            raise IdInCreateRequestException
        validation = QuestionUserSerializer(data=data)
        if not validation.is_valid():
            return validation.errors
        return None

    @action(detail=True, methods=('post',))
    def add_question(self, request: Request, pk: int):
        poll = get_object_or_404(Poll, pk=pk)
        data = request.data
        errors = self.validate_and_enrich_question_data(poll, data)
        if errors is not None:
            return JsonResponse(errors)
        data['poll'] = poll
        Question.objects.create(**data)
        return JsonResponse(PollDetailAdminSerializer(poll).data)

    @action(detail=True, methods=('get',), permission_classes=(IsAdminUser,), url_path='answers/(?P<user_pk>[\d+]+)')
    def user_answers(self, request: Request, pk, user_pk=None):
        # we cannot simply do zip between all the questions to current poll and all the answers to those questions,
        # because there can be questions without an answer because they were added after the user has sent his answers
        # This situation requires us to select for each answer a respective answer of null if not found
        #
        # If the user has not answered in this poll yet then all questions will have 'answer': null
        poll = get_object_or_404(Poll, pk=pk)
        answer = Answer.objects.filter(
            user_id=user_pk,
            question_id=OuterRef('pk')
        ).values_list('text', flat=True)[:1]  # getting last answer to every question
        questions = poll.questions.annotate(answer=Subquery(answer))
        return JsonResponse({
            'poll': PollCommonSerializer(poll).data,
            'questions_answers': QuestionWithAnswerSerializer(questions, many=True).data
        })
