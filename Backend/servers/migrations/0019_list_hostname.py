# Generated by Django 2.2.5 on 2019-10-07 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0018_auto_20191007_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='hostname',
            field=models.CharField(default='', max_length=250),
        ),
    ]
