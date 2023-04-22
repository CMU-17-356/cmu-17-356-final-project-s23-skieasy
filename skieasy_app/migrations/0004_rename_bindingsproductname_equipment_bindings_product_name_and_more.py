# Generated by Django 4.1.6 on 2023-04-22 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skieasy_app', '0003_alter_equipmentlisting_equipmentid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='bindingsProductName',
            new_name='bindings_product_name',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='bootSize',
            new_name='boot_size',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='bootsProductName',
            new_name='boots_product_name',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='equipmentHeight',
            new_name='equipment_height',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='equipmentProductName',
            new_name='equipment_product_name',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='equipmentType',
            new_name='equipment_type',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='profileId',
            new_name='profile_id',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='skillLevel',
            new_name='skill_level',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='wearStatus',
            new_name='wear_status',
        ),
        migrations.RenameField(
            model_name='equipmentimages',
            old_name='equipmentId',
            new_name='equipment_id',
        ),
        migrations.RenameField(
            model_name='equipmentlisting',
            old_name='endDate',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='equipmentlisting',
            old_name='equipmentId',
            new_name='equipment_id',
        ),
        migrations.RenameField(
            model_name='equipmentlisting',
            old_name='profileId',
            new_name='profile_id',
        ),
        migrations.RenameField(
            model_name='equipmentlisting',
            old_name='startDate',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='equipmentreservation',
            old_name='endDate',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='equipmentreservation',
            old_name='equipmentId',
            new_name='equipment_id',
        ),
        migrations.RenameField(
            model_name='equipmentreservation',
            old_name='profileId',
            new_name='profile_id',
        ),
        migrations.RenameField(
            model_name='equipmentreservation',
            old_name='startDate',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='bootSize',
            new_name='boot_size',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='firstName',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='lastName',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='userType',
            new_name='user_type',
        ),
    ]
