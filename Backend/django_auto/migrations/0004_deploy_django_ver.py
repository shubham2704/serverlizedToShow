# Generated by Django 2.2.5 on 2019-09-29 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_auto', '0003_deploy'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploy',
            name='django_ver',
            field=models.CharField(default='', max_length=250),
        ),
    ]
