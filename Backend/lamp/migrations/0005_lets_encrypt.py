# Generated by Django 2.2.5 on 2019-09-18 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0011_auto_20190918_0023'),
        ('signup', '0004_projects'),
        ('lamp', '0004_ssl'),
    ]

    operations = [
        migrations.CreateModel(
            name='lets_encrypt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=45)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lamp.domain')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servers.list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.user')),
            ],
        ),
    ]
