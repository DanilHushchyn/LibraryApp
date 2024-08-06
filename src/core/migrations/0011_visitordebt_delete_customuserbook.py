# Generated by Django 5.0.7 on 2024-08-06 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_historicalbook'),
        ('users', '0008_alter_customuser_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorDebt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_took', models.DateField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.book')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts', to='users.visitor')),
            ],
            options={
                'verbose_name': 'Долг посетителя',
                'verbose_name_plural': 'Долги посетителей',
                'db_table': 'visitor_debts',
                'ordering': ['book__name'],
                'unique_together': {('book', 'visitor')},
            },
        ),
        migrations.DeleteModel(
            name='CustomUserBook',
        ),
    ]