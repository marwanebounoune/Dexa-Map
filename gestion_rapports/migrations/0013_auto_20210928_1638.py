# Generated by Django 3.2.7 on 2021-09-28 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_rapports', '0012_auto_20210928_1542'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='commentaire',
            unique_together=set(),
        ),
        migrations.AlterModelTable(
            name='commentaire',
            table='Rapport_commentaire',
        ),
    ]