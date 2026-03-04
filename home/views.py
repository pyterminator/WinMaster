import json
from django.shortcuts import render, redirect
from home.models import SocialMedia, RootColor, Sentence, Question, UserData, UserAnswer, Option
from django.http import JsonResponse

def index(request):
    success = request.session.pop("form_success", False)
    
    social_media_links = SocialMedia.objects.all()
    colors = RootColor.objects.all()
    sentences = Sentence.objects.all()

    data = {
        "social_media": social_media_links,
        "colors": colors,
        "sentences": sentences,
        "success":success
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
    colors = RootColor.objects.all()
    invalid = request.session.pop("form_invalid", False)
    if request.method == "POST":
        fullname = request.POST.get("fullname") 
        phone = request.POST.get("phone")
        mexfilik = request.POST.get("mexfilik")
        user_answer = request.POST.get("user_answer")
        user_answer = json.loads(user_answer)

        if not bool(mexfilik):
            request.session["form_invalid"] = True
            return redirect("registerpage")

        new_user_data = UserData(fullname=fullname, phone=phone)
        new_user_data.save()
        
        keys = user_answer.keys()
        for q_id in keys:
            opt_id = user_answer.get(q_id)
            question = Question.objects.filter(id=q_id).first()
            option = Option.objects.filter(id=opt_id).first()
            new_user_answer = UserAnswer(
                question=question,
                selected_option=option,
                user=new_user_data,
            )  

            new_user_answer.save()
        request.session["form_success"] = True
        return redirect("homepage")
            
        

    data={
        "colors": colors,
        "invalid":invalid
    }
    return render(request, "pages/register.html", context=data)