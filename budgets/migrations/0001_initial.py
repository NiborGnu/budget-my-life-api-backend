# Generated by Django 5.1.2 on 2024-11-17 21:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='budgets', to='categories.category')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='users.profile')),
            ],
        ),
    ]
