# Generated by Django 2.2.3 on 2019-07-22 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190722_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=6.99, max_digits=100, null=True),
        ),
    ]
