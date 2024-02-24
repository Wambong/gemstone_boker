# Generated by Django 5.0 on 2024-02-11 16:26

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]