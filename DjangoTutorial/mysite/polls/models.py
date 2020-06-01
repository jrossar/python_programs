import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

#each model is represented by a class that sublcasses models.Model
class Question(models.Model):
    #max length required for char field
    question_text = models.CharField(max_length=200)
    #first argument is human readable name
    pub_date = models.DateTimeField("date published")

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text