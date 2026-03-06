from django.db import models
from colorfield.fields import ColorField
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import strip_tags

class SocialMedia(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RootColor(models.Model):
    color_name = models.CharField(max_length=100)
    color_hex = ColorField(default='#FFFFFF')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.color_name

class Question(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({self.question.title})"

class Sentence(models.Model):
    text = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class UserData(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fullname} - {self.phone}"

class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)

    user = models.ForeignKey(UserData, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.question}"
    
class Mexfilik(models.Model):
    text = CKEditor5Field('Text', config_name='extends')

    def __str__(self):
        return f"Məxfilik siyasəti - {strip_tags(self.text)[:35]}..."