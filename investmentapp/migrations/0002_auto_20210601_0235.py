# Generated by Django 3.1.4 on 2021-06-01 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investmentapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invest',
            name='factor',
        ),
        migrations.DeleteModel(
            name='Conversion',
        ),
    ]