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
from django.contrib.auth.models import User

from .models import Quiz
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import pandas as pd
import json
import sqlite3

from django.views.decorators.http import require_POST

def accueil(request):
    return render(request, 'accueil.html')

def login_page(request):
    if request.method == 'POST':
        # Vérifier les identifiants de connexion
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if a user with the given username exists
        user = User.objects.get(username=username)

        # Check if the password matches
        if check_password(password, user.password):
            # Identifiants corrects, effectuer la redirection
            return redirect('accueil')  # Rediriger vers la page d'accueil
        else:
            # Identifiants incorrects, afficher un message d'erreur
            error_message = 'Nom d\'utilisateur ou mot de passe incorrect.'
            return render(request, 'login_page.html', {'error_message': error_message})
    return render(request, 'login_page.html')
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if the passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')  # Render the signup template again

        # Create the user
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login_page')  # Redirect to the login page
        except Exception as e:
            messages.error(request, str(e))  # Handle exceptions (e.g., username already taken)
            return render(request, 'signup.html')

    return render(request, 'signup.html')

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


def question_view(request, table_name=None):


    # If table_name is not provided, fetch the first table name from SERIE_QUIZ
    if table_name is None:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM SERIE_QUIZ LIMIT 1;")
        first_table = cursor.fetchone()
        if first_table:
            table_name = first_table[0]
        else:
            return JsonResponse({'error': 'No tables found.'}, status=404)
    # Your logic here, possibly fetching questions based on the table_name
    return render(request, 'quiz.html', {'current_question_index': 0, 'table_name': table_name})



def api_questions(request, table_name=None):
    # Connect to the SQLite database
    conn = sqlite3.connect('db.sqlite3')
    print(table_name)
    # If table_name is not provided, fetch the first table name from SERIE_QUIZ
    if table_name is None:
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM SERIE_QUIZ LIMIT 1;")
        first_table = cursor.fetchone()
        if first_table:
            table_name = first_table[0]
        else:
            return JsonResponse({'error': 'No tables found.'}, status=404)

    try:
        # Write a query to select all data from the specified table
        query = f"SELECT * FROM {table_name};"

        # Read the data into a Pandas DataFrame
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Return error if the query fails
    finally:
        # Ensure the connection is closed
        conn.close()

    def replace_nan_in_json(json_str):
        return json_str.replace('NaN', '"NaN"')

    # Apply the function to the 'propositions' column
    df['propositions'] = df['propositions'].apply(replace_nan_in_json)
    df['propositions'] = df['propositions'].apply(lambda x: f'[{x}]')

    # Convert the DataFrame to JSON
    json_data = df.to_json(orient='records')

    return JsonResponse(json_data, safe=False)

def serie_de_question_view(request):
    # Connect to the SQLite database
    conn = sqlite3.connect('db.sqlite3')

    try:
        # Create a cursor object
        cursor = conn.cursor()

        # Write a query to list all tables in the SERIE_QUIZ table
        query = "SELECT table_name FROM SERIE_QUIZ;"

        # Execute the query
        cursor.execute(query)

        # Fetch all results (list of tables)
        tables = cursor.fetchall()

        # Extract table names from tuples
        table_names = [table for table in tables]

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        table_names = []  # Default to an empty list on error

    finally:
        # Close the connection
        conn.close()

    # Pass the list of table names to the template
    return render(request, 'serie_de_question.html', {'tables': table_names})

def view_table(request, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Query to select all data from the specified table
    query = f"SELECT * FROM {table_name};"  # Using f-string for safe formatting

    try:
        cursor.execute(query)
        table_data = cursor.fetchall()  # Fetch all rows
        columns = [description[0] for description in cursor.description]  # Get column names
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        table_data = []  # Default to an empty list on error
        columns = []

    finally:
        conn.close()

    # Pass the columns and table data to the template
    return render(request, 'view_table.html', {'columns': columns, 'table_data': table_data})

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
    # Connect to the SQLite database
    connection = sqlite3.connect('db.sqlite3')

    # Sanitize file name for table creation (convert invalid characters to '_')
    table_name = re.sub(r'\W|^(?=\d)', '_', csv_file_name.split('.')[0])

    try:
        cursor = connection.cursor()

        # Drop the table if it exists (SQLite does not support CREATE OR REPLACE)
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Create the new table
        cursor.execute(f"""
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                propositions TEXT,
                correct_answer TEXT,
                explanation TEXT
            )
        """)

        # Create the SERIE_QUIZ table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SERIE_QUIZ (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL UNIQUE
            )
        """)

        # Insert the new table name into SERIE_QUIZ if not already present
        cursor.execute("""
            INSERT OR IGNORE INTO SERIE_QUIZ (table_name)
            VALUES (?)
        """, (table_name,))

        # Commit changes
        connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()
        connection.close()
@require_POST
def delete_serie_question(request, table_name):
    conn = sqlite3.connect('db.sqlite3')
    try:
        cursor = conn.cursor()

        # Supprimer la série de la table SERIE_QUIZ
        cursor.execute("DELETE FROM SERIE_QUIZ WHERE table_name = ?", (table_name,))
        conn.commit()

        # Si la requête vient d'AJAX, renvoyer JSON
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})

    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": str(e)})
    finally:
        conn.close()

    # Redirection si appel normal
    return render(request,'serie_de_question.html')
