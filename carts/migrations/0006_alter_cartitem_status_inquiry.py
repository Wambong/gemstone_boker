# Generated by Django 5.0 on 2024-02-10 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userprofile_profile_picture'),
        ('carts', '0005_alter_cartitem_status'),
        ('store', '0002_product_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='status',
            field=models.CharField(blank=True, choices=[('submit', 'Submit'), ('processing', 'Processing'), ('ready', 'Ready')], default='submit', max_length=250, null=True),
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('inquiry_date', models.DateTimeField(auto_now_add=True)),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiry_cart_items', to='carts.cartitem')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiry_variations', to='carts.cartitem')),
            ],
        ),
    ]