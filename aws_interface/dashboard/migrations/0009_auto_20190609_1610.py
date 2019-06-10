# Generated by Django 2.1.8 on 2019-06-09 07:10

import cloud.shortuuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_remove_log_app'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(default=cloud.shortuuid.uuid, editable=False, max_length=255, primary_key=True, serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(editable=False, max_length=255)),
                ('target', models.CharField(editable=False, max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('amount', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.CharField(default=cloud.shortuuid.uuid, editable=False, max_length=255, primary_key=True, serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('funnel', models.CharField(max_length=255, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='tracker_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Tracker'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
