# Generated by Django 3.2.7 on 2021-09-30 11:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_rapports', '0018_rapport_descriptif_sdb'),
    ]

    operations = [
        migrations.AddField(
            model_name='rapport',
            name='descriptif_climatiseur',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='rapport',
            name='descriptif_donne_sur',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='rapport',
            name='descriptif_orientation',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, null=True, size=None),
        ),
    ]