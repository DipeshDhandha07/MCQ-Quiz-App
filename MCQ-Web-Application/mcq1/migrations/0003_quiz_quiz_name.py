# Generated by Django 3.0.2 on 2020-03-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq1', '0002_question_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='quiz_name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
