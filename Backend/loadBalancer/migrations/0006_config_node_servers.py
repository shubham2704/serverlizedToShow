# Generated by Django 2.2.5 on 2019-10-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loadBalancer', '0005_auto_20191007_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='node_servers',
            field=models.CharField(default='', max_length=100),
        ),
    ]
