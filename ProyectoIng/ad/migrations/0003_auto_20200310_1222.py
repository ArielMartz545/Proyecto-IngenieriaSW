# Generated by Django 3.0.3 on 2020-03-10 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0002_auto_20200310_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ubication',
            name='correlative_direction',
            field=models.ForeignKey(blank=True, default='Ninguna', null=True, on_delete=django.db.models.deletion.CASCADE, to='ad.Ubication'),
        ),
    ]
