# Generated by Django 3.1.4 on 2020-12-09 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ztx', '0003_auto_20201119_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='金额'),
        ),
    ]
