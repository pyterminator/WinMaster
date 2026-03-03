from django.shortcuts import render
from home.models import SocialMedia, RootColor, Sentence, Question
from django.http import JsonResponse

def index(request):
    social_media_links = SocialMedia.objects.all()
    colors = RootColor.objects.all()
    sentences = Sentence.objects.all()

    data = {
        "social_media": social_media_links,
        "colors": colors,
        "sentences": sentences
    }

    return render(request, "pages/index.html", context=data)

def quiz(request):
    colors = RootColor.objects.all()  
    data = { 
        "colors": colors,
    }
    return render(request, "pages/quiz.html", context=data)

def get_quiz(request):
    questions = Question.objects.prefetch_related('options').all()
    data = [
        {
            "id": q.id,
            "title": q.title,
            "options": [{"id": o.id, "text": o.text} for o in q.options.all()]
        }
        for q in questions
    ]
    return JsonResponse(data, safe=False)

def register(request):
    return render(request, "pages/register.html")