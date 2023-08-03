from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#
class Usr(models.Model):

    user = models.OneToOneField(User, models.CASCADE, primary_key=True)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Quiz(models.Model):
    quiz_name = models.CharField(max_length=50, default=None)
    no_ques = models.IntegerField()
    author = models.ForeignKey('Usr', on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)

    def __str__(self):
        return self.quiz_name

class Question(models.Model):
    question = models.CharField(max_length=1000, default=None)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    mrk_correct = models.IntegerField()
    neg_mrk = models.IntegerField()
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    cor_choice = models.CharField(max_length=255)
