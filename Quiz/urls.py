from django.urls import path
from . import views

urlpatterns = [
    path('get_quizs/', views.get_quizs, name='get_quizs'),
    path('response_quiz/', views.response_quiz, name='response_quiz'),
    path('get_response_quizs/', views.get_response_quizs, name='get_response_quizs'),
    path('response_question/', views.response_question, name='response_question'),
]
