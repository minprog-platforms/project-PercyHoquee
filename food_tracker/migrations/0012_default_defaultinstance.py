# Generated by Django 3.2.9 on 2021-12-16 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_tracker', '0011_auto_20211216_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Default',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_tracker.meal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defaults', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DefaultInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='food_tracker.default')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_tracker.product')),
            ],
        ),
    ]
