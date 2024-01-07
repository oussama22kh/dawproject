from rest_framework import serializers
from .models import Questionnaire, Question, Option, ResponsesQuestionnaire, ResponsesQuestion


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'optionText', 'point')


class QuestionSerializer(serializers.ModelSerializer):
    Options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'questionText', 'questionType', 'Options')


class QuestionnaireSerializer(serializers.ModelSerializer):
    Questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'questionnaireName', 'dateOfTheQuestionnaire', 'Questions')


class ResponsesQuestionSerializer(serializers.ModelSerializer):
    option = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = ResponsesQuestion
        fields = ('id', 'id_Reponse_Questionnaire', 'id_Option', 'option')
        # extra_kwargs = {
        #     'id_Patient' : {'required':True,'allow_blank':False},
        #     'id_Questionnaire': {'required':True,'allow_blank':False},
        # }


class ReponseQuestionnaireSerializer(serializers.ModelSerializer):
    response_question = ResponsesQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = ResponsesQuestionnaire
        fields = '__all__'
        # extra_kwargs = {
        #     'id_Patient' : {'required':True,'allow_blank':False},
        #     'id_Questionnaire': {'required':True,'allow_blank':False},
        # }
