# Generated by Django 5.0.4 on 2024-08-04 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0009_lga_state_zone_alter_profile_nationality_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='sen_dist',
            new_name='senate_district',
        ),
    ]
