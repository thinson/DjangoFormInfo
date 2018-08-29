from django.contrib import admin
from .models import Questionnaire, Question, Answer

# Register your models here.
@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ("id", "paper_name", "created_time", "last_update_time")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_name", "author")

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "author", "answer_name")
