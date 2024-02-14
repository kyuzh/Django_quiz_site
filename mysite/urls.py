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
from myapp import views as myapp_views
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', myapp_views.login_page, name='login_page'),
    path('', never_cache(myapp_views.question_view), name='question_view'),
    path('import_csv/', myapp_views.import_csv, name='import_csv'),
    path('login_page/', myapp_views.login_page, name='login_page'),
    path('accueil/', myapp_views.accueil, name='accueil'),
    path('csv_diplay/', myapp_views.create_serie_quiz_view, name='create_serie_quiz'),
    path('serie_de_question', myapp_views.serie_de_question_view, name='serie_de_question'),
    path('question/<int:question_id>/', myapp_views.question_view, name='question_view'),
    path('answer/<int:question_id>/', myapp_views.answer_view, name='answer_view'),

]
