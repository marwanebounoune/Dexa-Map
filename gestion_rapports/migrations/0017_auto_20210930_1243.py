# Generated by Django 3.2.7 on 2021-09-30 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_rapports', '0016_auto_20210930_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rapport',
            name='descriptif_climatiseur',
        ),
        migrations.RemoveField(
            model_name='rapport',
            name='descriptif_donne_sur',
        ),
        migrations.RemoveField(
            model_name='rapport',
            name='descriptif_orientation',
        ),
        migrations.RemoveField(
            model_name='rapport',
            name='descriptif_sdb',
        ),
    ]
