# Generated by Django 2.1.7 on 2019-04-16 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0005_auto_20190416_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csv',
            name='documentFilename',
        ),
    ]