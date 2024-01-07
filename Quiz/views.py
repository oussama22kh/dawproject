from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Question, Questionnaire, Option, ResponsesQuestionnaire, ResponsesQuestion
from .serializers import QuestionnaireSerializer, QuestionSerializer, OptionSerializer, ReponseQuestionnaireSerializer, \
    ResponsesQuestionSerializer


# Create your views here.


@api_view(['GET'])
def get_quizs(request):
    questionnaires = Questionnaire.objects.all()
    serializers = QuestionnaireSerializer(questionnaires, many=True)
    return Response(
        {
            'Quizs': serializers.data
        }
    )


@api_view(['GET'])
def get_response_quizs(request):
    response_questionnaires = ResponsesQuestionnaire.objects.all()
    serializers = ReponseQuestionnaireSerializer(response_questionnaires, many=True)
    return Response(
        {
            'response_questionnaires': serializers.data
        }
    )


# Create your views here.


@api_view(['POST'])
# @login_required
def response_quiz(request):
    data = request.data
    response_q = ReponseQuestionnaireSerializer(data=data)

    if response_q.is_valid():

        validated_data = response_q.validated_data
        if not ResponsesQuestionnaire.objects.filter(id_Questionnaire=validated_data['id_Questionnaire'],
                                                     id_Patient=validated_data['id_Patient']).exists():

            data = ResponsesQuestionnaire.objects.create(
                id_Patient=validated_data['id_Patient'],
                id_Questionnaire=validated_data['id_Questionnaire']
            )
            return Response({
                "details": "Response is created successfully!",
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "details": "You already respose for this quiz!",
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(response_q.errors)


@api_view(['POST'])
def response_question(request):
    data = request.data
    response_q = ResponsesQuestionSerializer(data=data)

    if response_q.is_valid():
        validated_data = response_q.validated_data
        data = ResponsesQuestion.objects.create(
            id_Reponse_Questionnaire=validated_data['id_Reponse_Questionnaire'],
            id_Option=validated_data['id_Option']
        )

        return Response({
            "details": "Response is created successfully!",
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(response_q.errors, status=status.HTTP_400_BAD_REQUEST)
