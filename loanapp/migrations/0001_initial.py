# Generated by Django 4.0.1 on 2022-01-13 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_cuota', models.FloatField()),
                ('amount_deuda', models.FloatField()),
            ],
        ),
    ]
