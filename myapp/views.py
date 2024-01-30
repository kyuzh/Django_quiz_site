import csv
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.db import transaction

from .models import Question, Choice, Quiz
import pandas as pd

def accueil(request):
    return render(request, 'myapp/accueil.html')

def login_page(request):
    if request.method == 'POST':
        # Vérifier les identifiants de connexion
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '1234' and password == '1234':
            # Identifiants corrects, effectuer la redirection
            return redirect('accueil')  # Rediriger vers la page d'accueil
        else:
            # Identifiants incorrects, afficher un message d'erreur
            error_message = 'Nom d\'utilisateur ou mot de passe incorrect.'
            return render(request, 'myapp/login_page.html', {'error_message': error_message})
    return render(request, 'myapp/login_page.html')

def import_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if csv_file:
            # Vérifier si le fichier est un fichier CSV
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Veuillez sélectionner un fichier CSV.')
                return HttpResponseRedirect(reverse('accueil'))  # Rediriger vers la page d'accueil ou une autre vue appropriée

            # Lire et traiter le fichier CSV
            csv_data = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(csv_data)

            # Stocker les lignes du CSV dans une liste
            csv_rows = list(reader)

            # Vous pouvez effectuer d'autres opérations de traitement ici

            # Passer les données CSV à la template pour l'affichage
            context = {'csv_rows': csv_rows}
            return render(request, 'myapp/csv_display.html', context)

    # Si la méthode de requête n'est pas POST, afficher simplement la page avec le formulaire d'importation de fichier
    return render(request, 'myapp/import_csv.html')

def question_view(request, question_id):
    question = Question.objects.get(pk=question_id)
    choices = question.choice_set.all()
    context = {'question': question, 'choices': choices}
    return render(request, 'myapp/quiz.html', context)

def answer_view(request, question_id):
    selected_choice_id = request.POST['choice']
    selected_choice = Choice.objects.get(pk=selected_choice_id)
    if selected_choice.is_correct:
        response = "Correct!"
    else:
        response = "Incorrect!"
    return HttpResponse(response)


def create_choices_for_question(question_text,choices):
    quiz = Quiz(title=question_text, description=",".join(choices))
    quiz.save()

    # Vous pouvez également accéder aux attributs de l'objet Quiz si nécessaire
    print("ID du quiz créé :", quiz.id)
    print("Titre du quiz :", quiz.title)
    print("Description du quiz :", quiz.description)

def create_serie_quiz(request):
    if request.method == 'POST':
        question_text = request.POST.get('dropdown1')
        choices = []
        for i in range(2, 5):
            choice_text = request.POST.get('dropdown{}'.format(i))
            if choice_text:
                choices.append(choice_text)

        create_choices_for_question(question_text, choices)

        return render(request, 'myapp/accueil.html')

    return render(request, 'myapp/csv_display.html')
