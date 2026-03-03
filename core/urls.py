from django.contrib import admin
from django.urls import path, include
from home.views import index, quiz, get_quiz

urlpatterns = [
    path('', index, name='homepage'),
    path('question', quiz, name='quizpage'),
    path('getquiz', get_quiz, name='getquiz'),
    path('admin/', admin.site.urls),
]
