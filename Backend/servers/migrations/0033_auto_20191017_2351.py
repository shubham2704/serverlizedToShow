# Generated by Django 2.2.5 on 2019-10-17 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0032_billing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='Charges',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=10),
        ),
    ]
