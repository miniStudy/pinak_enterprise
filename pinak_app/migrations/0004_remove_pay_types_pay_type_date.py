# Generated by Django 5.1.3 on 2024-12-16 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinak_app', '0003_alter_project_types_project_type_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pay_types',
            name='pay_type_date',
        ),
    ]