# Generated by Django 5.1.3 on 2024-12-21 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinak_app', '0023_alter_project_expense_bank_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_day_details',
            name='project_day_detail_machine_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pinak_app.machines'),
        ),
    ]