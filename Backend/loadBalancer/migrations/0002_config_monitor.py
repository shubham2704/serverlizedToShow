# Generated by Django 2.2.5 on 2019-10-07 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loadBalancer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='monitor',
            field=models.BooleanField(default=False),
        ),
    ]
