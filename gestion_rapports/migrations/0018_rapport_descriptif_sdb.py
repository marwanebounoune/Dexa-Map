# Generated by Django 3.2.7 on 2021-09-30 11:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_rapports', '0017_auto_20210930_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='rapport',
            name='descriptif_sdb',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, null=True, size=None),
        ),
    ]
