# Generated by Django 3.2.7 on 2021-09-28 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_rapports', '0008_rename_photographie_photographierapport'),
    ]

    operations = [
        migrations.AddField(
            model_name='photographierapport',
            name='rapport',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_rapports.rapport'),
        ),
    ]
