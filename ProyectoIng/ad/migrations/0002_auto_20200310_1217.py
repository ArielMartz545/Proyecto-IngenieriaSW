# Generated by Django 3.0.3 on 2020-03-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ubication',
            name='id',
        ),
        migrations.AddField(
            model_name='ubication',
            name='direction',
            field=models.CharField(default='Ninguna', max_length=50, primary_key=True, serialize=False),
        ),
    ]
