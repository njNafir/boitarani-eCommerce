# Generated by Django 2.1.7 on 2019-03-27 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_product_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-timestamp',)},
        ),
    ]
