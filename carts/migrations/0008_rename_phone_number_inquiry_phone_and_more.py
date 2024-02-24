# Generated by Django 5.0 on 2024-02-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_alter_inquiry_country_alter_inquiry_seller'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inquiry',
            old_name='phone_number',
            new_name='phone',
        ),
        migrations.RemoveField(
            model_name='inquiry',
            name='variation',
        ),
        migrations.AddField(
            model_name='inquiry',
            name='inquiry_note',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='inquiry_number',
            field=models.CharField(default='123', max_length=120),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='is_submitted',
            field=models.BooleanField(default=False),
        ),
    ]
