# Generated by Django 3.0.5 on 2020-04-17 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('images', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_kind', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Tipo de Anuncio',
                'verbose_name_plural': 'Tipos de Anuncio',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_description', models.TextField()),
                ('category_icon_class', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=100)),
                ('currency_sign', models.CharField(max_length=5)),
            ],
            options={
                'verbose_name': 'Moneda',
                'verbose_name_plural': 'Monedas',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_type', models.CharField(default='Unidad', max_length=10)),
            ],
            options={
                'verbose_name': 'Unidad',
                'verbose_name_plural': 'Unidades',
            },
        ),
        migrations.CreateModel(
            name='PriceRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_price', models.FloatField()),
                ('max_price', models.FloatField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.Currency')),
            ],
            options={
                'verbose_name': 'Rango de Precio',
                'verbose_name_plural': 'Rangos de Precio',
            },
        ),
        migrations.CreateModel(
            name='CurrencyConversion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_equals', models.FloatField()),
                ('currency_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_one', to='ad.Currency')),
                ('currency_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_two', to='ad.Currency')),
            ],
            options={
                'verbose_name': 'Conversión de Moneda',
                'verbose_name_plural': 'Conversiones de Moneda',
            },
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_name', models.CharField(max_length=100)),
                ('ad_description', models.TextField()),
                ('price', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('ad_images', models.ManyToManyField(related_name='get_images_ad', to='images.Image')),
                ('id_ad_kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.AdKind')),
                ('id_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.Category')),
                ('id_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.Currency')),
                ('id_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.Location')),
                ('id_store', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Store')),
                ('id_unit', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ad.Unit')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Anuncio',
                'verbose_name_plural': 'Anuncios',
            },
        ),
    ]
