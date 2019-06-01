# Generated by Django 2.2 on 2019-06-01 03:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190528_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 1, 9, 13, 55, 991666)),
        ),
        migrations.AlterField(
            model_name='posts',
            name='post_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 1, 9, 13, 55, 990666)),
        ),
        migrations.CreateModel(
            name='user_request',
            fields=[
                ('token', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('hash', models.CharField(default=None, max_length=64, null=True)),
            ],
            options={
                'unique_together': {('token', 'hash')},
            },
        ),
    ]