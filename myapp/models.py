from django.db import models
import random

# Create your models here.
class Quiz(models.Model):
    number_of_questions = models.IntegerField()
    topic = models.CharField(max_length=120)
    title = models.CharField(max_length=255)
    file_csv = models.CharField(max_length=120)
    # time = models.IntegerField(help_text="duration of the quiz in minutes")
    # required_score_to_pass = models.IntegerField(help_text="required score in %")
    description = models.TextField()

    def __str__(self):
        return self.title


    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'

class Question(models.Model):
    text = models.CharField(max_length=200)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    correct_choice = models.CharField(max_length=200)



