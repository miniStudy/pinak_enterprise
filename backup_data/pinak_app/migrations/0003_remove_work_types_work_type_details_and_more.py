# Generated by Django 5.1.5 on 2025-02-23 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinak_app', '0002_alter_project_material_data_project_material_material_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work_types',
            name='work_type_details',
        ),
        migrations.AddField(
            model_name='company_details',
            name='company_sharuaati_shilak',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
