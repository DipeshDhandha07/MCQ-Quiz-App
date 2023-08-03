from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('edit_quiz/', views.edit_quiz, name='edit_quiz'),
    path('edit_quiz/(?P<pk>/d+)/', views.edit_quiz_pk, name='edit_quiz_pk'),
    path('add_question/', views.add_question, name='add_question'),
    path('take_quiz/(?P<pk>/d+)/', views.take_quiz, name='take_quiz'),
    path('attempt_ques/(?P<pk>/d+)/', views.attempt_ques, name='attempt_ques'),
    path('profile/(?P<pk>/d+)', views.profile, name='profile'),
    path('show_score/', views.show_score, name='show_score'),
]