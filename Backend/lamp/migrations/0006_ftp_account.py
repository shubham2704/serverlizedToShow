# Generated by Django 2.2.5 on 2019-09-23 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0004_projects'),
        ('servers', '0011_auto_20190918_0023'),
        ('lamp', '0005_lets_encrypt'),
    ]

    operations = [
        migrations.CreateModel(
            name='ftp_account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=100)),
                ('folder', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=45)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servers.list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.user')),
            ],
        ),
    ]
