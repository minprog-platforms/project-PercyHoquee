# Generated by Django 3.2.9 on 2021-12-14 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_tracker', '0007_auto_20211213_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(choices=[('ml.', 'ml.'), ('gr.', 'gr.')], max_length=3),
        ),
    ]
