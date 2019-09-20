# Generated by Django 2.2.5 on 2019-09-17 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0009_pkg_inst_data_viewpkgoption'),
        ('signup', '0004_projects'),
        ('lamp', '0003_auto_20190912_2231'),
    ]

    operations = [
        migrations.CreateModel(
            name='ssl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.CharField(max_length=1000)),
                ('private_key', models.CharField(max_length=1000)),
                ('status', models.CharField(max_length=25)),
                ('expiry', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lamp.domain')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servers.list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.user')),
            ],
        ),
    ]
