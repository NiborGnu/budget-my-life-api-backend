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
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('transaction_type', models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], max_length=7)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='categories.category')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='users.profile')),
                ('subcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='categories.subcategory')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
