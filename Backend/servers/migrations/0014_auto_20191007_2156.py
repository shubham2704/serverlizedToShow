# Generated by Django 2.2.5 on 2019-10-07 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0013_auto_20191007_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='parent_server',
            field=models.ForeignKey(blank=True, default="", null=True, on_delete=django.db.models.deletion.CASCADE, to='servers.list'),
        ),
    ]
