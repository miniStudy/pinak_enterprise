# Generated by Django 5.1.3 on 2024-12-23 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinak_app', '0004_alter_project_machine_data_project_machine_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_expense',
            name='project_expense_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]