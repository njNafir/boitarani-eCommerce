# Generated by Django 2.1.7 on 2019-04-19 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_remove_billingprofile_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='customer_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
