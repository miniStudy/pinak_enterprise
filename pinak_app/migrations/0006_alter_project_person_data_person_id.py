# Generated by Django 5.1.5 on 2025-02-23 14:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinak_app', '0005_alter_project_person_data_project_machine_data_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_person_data',
            name='person_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pinak_app.person'),
        ),
    ]
