# Generated by Django 2.1.7 on 2019-05-06 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20190506_0137'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='upload_product_file_path/')),
                ('product', models.ForeignKey(on_delete='product', to='products.Product')),
            ],
        ),
    ]
