# Generated by Django 5.0 on 2024-02-08 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='status',
            field=models.CharField(blank=True, choices=[('submit', 'submit'), ('processing', 'Processing'), ('ready', 'Ready')], default='submit', max_length=20, null=True),
        ),
    ]
