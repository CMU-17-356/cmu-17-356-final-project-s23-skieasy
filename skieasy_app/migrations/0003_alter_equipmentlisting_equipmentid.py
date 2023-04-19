# Generated by Django 4.1.6 on 2023-04-18 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skieasy_app', '0002_profile_firstname_profile_lastname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentlisting',
            name='equipmentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='equipment_listings', to='skieasy_app.equipment'),
        ),
    ]