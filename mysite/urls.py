"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import question_view, api_questions,import_csv, login_page, accueil, create_serie_quiz_view,\
serie_de_question_view
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', login_page, name='login_page'),
    path('', never_cache(question_view), name='question_view'),
    path('import_csv/', import_csv, name='import_csv'),
    path('login_page/', login_page, name='login_page'),
    path('accueil/', accueil, name='accueil'),
    path('csv_diplay/', create_serie_quiz_view, name='create_serie_quiz'),
    path('serie_de_question', serie_de_question_view, name='serie_de_question'),
    path('api/questions/', api_questions, name='api_questions'),


]
