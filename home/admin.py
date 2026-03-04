from django.contrib import admin
from home.models import SocialMedia, RootColor, Question, Option, Sentence, UserData, UserAnswer

admin.site.register(SocialMedia)
admin.site.register(RootColor)
admin.site.register(Sentence)
admin.site.register(UserData)
admin.site.register(UserAnswer)


class OptionInline(admin.TabularInline):
    model = Option
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]