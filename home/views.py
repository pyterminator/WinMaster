import json
import os 
import requests
from django.shortcuts import render, redirect
from home.models import SocialMedia, RootColor, Sentence, Question, UserData, UserAnswer, Option, Mexfilik
from django.http import JsonResponse
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

def escape_md_v2(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!/"
    for ch in escape_chars:
        text = text.replace(ch, f"\\{ch}")
    return text


def send_telegram_message(text):
    chat_ids = get_chat_ids()
    print(chat_ids)
    KEY = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{KEY}/sendMessage"
    
    safe_text = escape_md_v2(text)

    for chat_id in chat_ids:
        if not chat_id:
            continue
        data = {
            "chat_id": chat_id,
            "text": safe_text,
            "parse_mode": "MarkdownV2",
            "timeout":10
        }
        requests.post(url, json=data)


def get_chat_ids():
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    CHAT_ID2 = os.getenv("TELEGRAM_CHAT_ID2")
    chat_ids = [CHAT_ID, CHAT_ID2]
    return chat_ids



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
    mexf = Mexfilik.objects.last()
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
        interests = ""
        for q_id in keys:
            opt_id = user_answer.get(q_id)
            question = Question.objects.filter(id=q_id).first()
            option = Option.objects.filter(id=opt_id).first()
            interests += f"{question.title}: {option.text}\n"
            new_user_answer = UserAnswer(
                question=question,
                selected_option=option,
                user=new_user_data,
            )  

            new_user_answer.save()
        request.session["form_success"] = True
        send_telegram_message(
            f"Yeni qeydiyyat\nAd, Soyad: {new_user_data.fullname}\nTelefon: {new_user_data.phone}\n{interests}".strip()
        )
        return redirect("homepage")
            
        

    data={
        "colors": colors,
        "invalid":invalid,
        "mexfilik":mexf
    }
    return render(request, "pages/register.html", context=data)