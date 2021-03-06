# Generated by Django 2.2.5 on 2019-09-08 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0004_projects'),
        ('servers', '0003_auto_20190908_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='project_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='signup.projects'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='list',
            name='server_ip',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
    ]
