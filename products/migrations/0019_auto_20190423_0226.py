# Generated by Django 2.1.7 on 2019-04-22 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('vagitable', 'Vagitable'), ('book', 'book'), ('electronic', 'Electronic'), ('mens fashion', 'Mens fashion'), ('womens fashion', 'Womens fashion'), ('home appliences', 'Home appliences'), ('helth', 'Helth'), ('outdoor', 'Outdoor')], default='vagitable', max_length=120),
        ),
    ]
