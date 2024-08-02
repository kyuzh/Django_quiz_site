import csv
import os
import re
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.db import transaction
from django.conf import settings
from django.db import connection
from django.http import JsonResponse

from .models import Quiz
from django.views.decorators.csrf import csrf_protect
import pandas as pd
import json
import sqlite3
def accueil(request):
    return render(request, 'accueil.html')

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
            return render(request, 'login_page.html', {'error_message': error_message})
    return render(request, 'login_page.html')

def import_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if csv_file:
            # Vérifier si le fichier est un fichier CSV
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Veuillez sélectionner un fichier CSV.')
                return HttpResponseRedirect(reverse('import_csv'))  # Rediriger vers la page d'importation

            # Save the uploaded file to a specified location
            file_path = os.path.join(settings.MEDIA_ROOT, csv_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            # Read and process the CSV file
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                csv_rows = list(reader)

            # Pass the CSV data and file name to the template for display
            context = {'csv_rows': csv_rows, 'csv_file_name': csv_file.name}
            return render(request, 'csv_display.html', context)

    # Si la méthode de requête n'est pas POST, afficher simplement la page avec le formulaire d'importation de fichier
    return render(request, 'import_csv.html')


def question_view(request):
    # Envoyer les données au template
    return render(request, 'quiz.html', {'current_question_index': 0})

def api_questions(request):
    # Se connecter à la base de données SQLite
    conn = sqlite3.connect('db.sqlite3')

    # Écrire une requête SQL
    query = "SELECT * FROM examen_topic_google_data_engineer___工作表1;"

    # Lire les données de la base de données SQLite dans un DataFrame Pandas
    df = pd.read_sql_query(query, conn)

    def replace_nan_in_json(json_str):
        # Remplacer 'NaN' sans guillemets par '"NaN"'
        return json_str.replace('NaN', '"NaN"')

    # Appliquer la fonction à la colonne 'propositions'
    df['propositions'] = df['propositions'].apply(replace_nan_in_json)

    df['propositions'] = df['propositions'].apply(lambda x: f'[{x}]')
    # Convertir le DataFrame en JSON
    json_data = df.to_json(orient='records')

    # Fermer la connexion
    conn.close()

    return JsonResponse(json_data, safe=False)
def serie_de_question_view(request):

    return render(request, 'serie_de_question.html')


@csrf_protect
def create_serie_quiz_view(request):
    if request.method == 'POST':
        question = request.POST.get('dropdown1')
        propositions = request.POST.getlist('dropdown2')  # Use getlist for multiple select
        correct_answer = request.POST.get('dropdown3')
        explanation = request.POST.get('dropdown4')
        csv_file_name = request.POST.get('csv_file_name')

        create_table_from_csv(csv_file_name)
        # Sanitize file name for table creation
        table_name = re.sub(r'\W|^(?=\d)', '_', csv_file_name.split('.')[0])

        # Path to the CSV file in MEDIA_ROOT
        csv_file_path = os.path.join(settings.MEDIA_ROOT, csv_file_name)

        # Read the CSV file using pandas
        df = pd.read_csv(csv_file_path)

        # Optionally, print the DataFrame for debugging
        print(df.head())
        # Insert data into the dynamically created table
        with connection.cursor() as cursor:
            for index, row in df.iterrows():
                # Combine propositions columns into a dictionary
                propositions_dict = {}
                # Extract the propositions columns and format them
                for col in propositions:
                    propositions_dict[col] = row[col]
                propositions_json = json.dumps(propositions_dict)

                cursor.execute(f"""
                           INSERT INTO {table_name} (question, propositions, correct_answer, explanation)
                           VALUES (%s, %s, %s, %s)
                       """, [row.get(question, question), propositions_json,
                             row.get(correct_answer, None), row.get(explanation, None)])

        return redirect(reverse('accueil'))  # Redirect to a success page

    # If not a POST request, render the form template
    return render(request, 'csv_display.html', {'csv_rows': csv_rows})


def create_table_from_csv(csv_file_name):
    # Sanitize file name for table creation
    table_name = re.sub(r'\W|^(?=\d)', '_', csv_file_name.split('.')[0])

    # Drop table if it exists
    with connection.cursor() as cursor:
        cursor.execute(f"""
            DROP TABLE IF EXISTS {table_name}
        """)

    # Create table dynamically
    with connection.cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                propositions TEXT,
                correct_answer TEXT,
                explanation TEXT
            )
        """)