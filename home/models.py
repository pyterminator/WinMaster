from django.db import models
from colorfield.fields import ColorField

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

