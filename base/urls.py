from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('delete-resource/<str:pk>/', views.deleteResource, name="delete-resource"),

    path('ajax/room/<str:pk>/messages/', views.roomMessagesAjax, name="ajax-room-messages"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('room/<str:pk>/create-quiz/', views.create_quiz, name="create-quiz"),
    path('quiz/<str:pk>/', views.quiz_detail, name="quiz-detail"),
    path('delete-quiz/<str:pk>/', views.delete_quiz, name="delete-quiz"),
    path('delete-question/<str:pk>/', views.delete_question, name="delete-question"),
    path('create-quiz/', views.create_quiz_general, name="create-quiz-general"),
    path('quizzes/', views.quizzesPage, name="quizzes"),
]

