# Generated by Django 2.1.7 on 2019-05-07 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_productfile_namet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productfile',
            old_name='nameT',
            new_name='name',
        ),
    ]