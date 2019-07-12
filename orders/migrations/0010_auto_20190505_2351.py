# Generated by Django 2.1.7 on 2019-05-05 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_productpurchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpurchase',
            name='user',
        ),
        migrations.AddField(
            model_name='productpurchase',
            name='order_id',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]