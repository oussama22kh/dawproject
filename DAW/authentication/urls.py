from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup.as_view()),
    path('signin/', views.signin.as_view()),
    path('signout/', views.signout.as_view())

]
