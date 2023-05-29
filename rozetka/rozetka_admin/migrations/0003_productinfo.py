# Generated by Django 4.2.1 on 2023-05-27 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rozetka_admin', '0002_links_alter_keywords_options_alter_keywords_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('current_price', models.CharField(max_length=50)),
                ('pure_price', models.CharField(max_length=50)),
                ('link', models.TextField()),
                ('reviews', models.CharField(max_length=50)),
                ('features', models.TextField()),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
    ]