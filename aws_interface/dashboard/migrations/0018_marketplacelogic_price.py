# Generated by Django 2.1.9 on 2019-06-22 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_auto_20190620_0343'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketplacelogic',
            name='price',
            field=models.BigIntegerField(default=0),
        ),
    ]
