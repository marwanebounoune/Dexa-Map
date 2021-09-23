# Generated by Django 3.2.7 on 2021-09-23 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_map', '0004_auto_20210921_1325'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='pin',
            name='DEXA_usernam_14525c_idx',
        ),
        migrations.RemoveIndex(
            model_name='pin',
            name='DEXA_deleted_2c083c_idx',
        ),
        migrations.RemoveIndex(
            model_name='pin',
            name='DEXA_is_vali_e4ca93_idx',
        ),
        migrations.RemoveIndex(
            model_name='pin',
            name='DEXA_region__bf8e53_idx',
        ),
        migrations.RemoveIndex(
            model_name='pin',
            name='DEXA_type_de_f97af3_idx',
        ),
        migrations.RemoveIndex(
            model_name='pin',
            name='DEXA_type_de_f39be2_idx',
        ),
        migrations.AddIndex(
            model_name='pin',
            index=models.Index(fields=['username'], name='api_map_pin_usernam_781a3f_idx'),
        ),
        migrations.AddIndex(
            model_name='pin',
            index=models.Index(fields=['deleted'], name='api_map_pin_deleted_d56185_idx'),
        ),
        migrations.AddIndex(
            model_name='pin',
            index=models.Index(fields=['is_validate_by_user'], name='api_map_pin_is_vali_acd519_idx'),
        ),
        migrations.AddIndex(
            model_name='pin',
            index=models.Index(fields=['region'], name='api_map_pin_region__9a3621_idx'),
        ),
        migrations.AddIndex(
            model_name='pin',
            index=models.Index(fields=['type_de_reference'], name='api_map_pin_type_de_d867f0_idx'),
        ),
        migrations.AddIndex(
            model_name='pin',
            index=models.Index(fields=['type_de_bien'], name='api_map_pin_type_de_457e37_idx'),
        ),
        migrations.AlterModelTable(
            name='pin',
            table=None,
        ),
    ]
