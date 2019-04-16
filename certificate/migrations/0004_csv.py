# Generated by Django 2.1.7 on 2019-04-16 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0003_auto_20190414_1259'),
    ]

    operations = [
        migrations.CreateModel(
            name='csv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csvfile', models.FileField(upload_to='userfiles/')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificate.Templates')),
            ],
        ),
    ]