from django.db import models
import random

# Create your models here.
class Quiz(models.Model):
    question = models.CharField(max_length=2048)
    propositions = models.TextField()  # TextField to store multiple propositions
    correct_answer = models.CharField(max_length=120)
    explanation = models.CharField(max_length=1024)

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizzes'



