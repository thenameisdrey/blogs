# Generated by Django 2.0.7 on 2018-08-04 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0003_auto_20180804_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lab',
            name='topic_id',
        ),
    ]
