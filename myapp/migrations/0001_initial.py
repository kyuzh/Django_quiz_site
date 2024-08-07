# Generated by Django 4.2.14 on 2024-07-23 20:01

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.CharField(max_length=2048)),
                ("propositions", models.TextField()),
                ("correct_answer", models.CharField(max_length=120)),
                ("explanation", models.CharField(max_length=1024)),
            ],
            options={
                "verbose_name_plural": "Quizzes",
            },
        ),
    ]
