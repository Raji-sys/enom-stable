# Generated by Django 5.0.4 on 2024-08-04 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_duties'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='duties',
            options={'verbose_name_plural': 'Duties and responsibilities'},
        ),
        migrations.AddField(
            model_name='post',
            name='department',
            field=models.ForeignKey(blank=True, max_length=300, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_dept', to='staff.department'),
        ),
        migrations.AlterField(
            model_name='duties',
            name='department',
            field=models.ForeignKey(blank=True, max_length=300, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dept_duties', to='staff.department'),
        ),
    ]