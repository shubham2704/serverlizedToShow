# Generated by Django 2.2.5 on 2019-10-11 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loadBalancer', '0012_remove_replicate_file_subdomain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='domain_insert_withftp_dict',
            field=models.TextField(default=''),
        ),
    ]
