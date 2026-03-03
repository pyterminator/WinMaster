from django.contrib import admin
from home.models import SocialMedia, RootColor, Question, Option, Sentence

admin.site.register(SocialMedia)
admin.site.register(RootColor)
admin.site.register(Sentence)


class OptionInline(admin.TabularInline):
    model = Option
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]