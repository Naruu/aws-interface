# Generated by Django 2.1.8 on 2019-05-31 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20190508_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='app',
        ),
    ]