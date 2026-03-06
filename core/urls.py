from django.contrib import admin
from django.urls import path, include
from home.views import index, quiz, get_quiz, register

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='homepage'),
    path('question', quiz, name='quizpage'),
    path('register', register, name="registerpage"),
    path('getquiz', get_quiz, name='getquiz'),
    path('admin/', admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)