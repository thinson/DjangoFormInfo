from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Questionnaire(models.Model):
    paper_name = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.paper_name

class Question(models.Model):
    question_name = models.CharField(max_length=50)
    question_sheet = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<问题： %s>" % self.question_name

    class Meta:
        ordering = ['created_time']

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    question_sheet = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)
    answer_name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    answer_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<答案:  %s>" % self.answer_name
