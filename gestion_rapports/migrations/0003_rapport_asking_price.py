# Generated by Django 3.2.7 on 2021-09-27 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_rapports', '0002_auto_20210927_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='rapport',
            name='asking_price',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
