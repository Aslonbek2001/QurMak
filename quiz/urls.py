from django.urls import path
from .views import AllQuiz, MarathonView, ExamView # TestApiView
urlpatterns = [
    path('level/', MarathonView.as_view()),
    path('level/<int:level>/', AllQuiz.as_view()),
    path("exam/", ExamView.as_view())

]
