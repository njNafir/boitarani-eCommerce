# Generated by Django 2.1.7 on 2019-05-05 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_product_is_digital'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-timestamp']},
        ),
    ]
