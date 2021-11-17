from rest_framework import serializers

from polls.models import Poll, Question


class QuestionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('text', 'question_type')


class QuestionAdminSerializer(QuestionUserSerializer):
    class Meta(QuestionUserSerializer.Meta):
        fields = QuestionUserSerializer.Meta.fields + ('id',)
        read_only_fields = ('id',)


class QuestionWithAnswerSerializer(QuestionAdminSerializer):
    answer = serializers.CharField()

    class Meta(QuestionAdminSerializer.Meta):
        fields = QuestionAdminSerializer.Meta.fields + ('answer',)
        read_only_fields = ('id',)


class PollDetailSerializer(serializers.ModelSerializer):
    questions = QuestionUserSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'questions')
        read_only_fields = ('id',)

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        poll = Poll.objects.create(**validated_data)
        for question in questions_data:
            Question.objects.create(poll=poll, **question)
        return poll


class PollDetailAdminSerializer(PollDetailSerializer):
    questions = QuestionAdminSerializer(many=True)


class PollCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_date', 'end_date', 'description')
        read_only_fields = ('id', 'start_date')
