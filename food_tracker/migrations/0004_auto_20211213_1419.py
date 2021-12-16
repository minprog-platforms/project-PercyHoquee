# Generated by Django 3.2.9 on 2021-12-13 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_tracker', '0003_auto_20211213_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='breakfast',
            name='meal',
        ),
        migrations.RemoveField(
            model_name='breakfast',
            name='product',
        ),
        migrations.RemoveField(
            model_name='dinner',
            name='meal',
        ),
        migrations.RemoveField(
            model_name='dinner',
            name='product',
        ),
        migrations.RemoveField(
            model_name='lunch',
            name='meal',
        ),
        migrations.RemoveField(
            model_name='lunch',
            name='product',
        ),
        migrations.RemoveField(
            model_name='snacks',
            name='meal',
        ),
        migrations.RemoveField(
            model_name='snacks',
            name='product',
        ),
        migrations.CreateModel(
            name='ProductInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('breakfast_item', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='food_tracker.breakfast')),
                ('dinner_item', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='food_tracker.dinner')),
                ('lunch_item', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='food_tracker.lunch')),
                ('snack_item', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='food_tracker.snacks')),
            ],
        ),
    ]
