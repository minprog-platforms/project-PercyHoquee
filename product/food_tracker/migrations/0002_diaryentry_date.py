# Generated by Django 3.2.9 on 2021-12-13 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaryentry',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
