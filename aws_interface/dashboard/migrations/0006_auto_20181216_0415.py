# Generated by Django 2.1.4 on 2018-12-16 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20181215_1102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='aes_key_salt',
            new_name='salt',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password_salt',
        ),
    ]