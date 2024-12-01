# Generated by Django 5.1.3 on 2024-11-28 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinak_app', '0002_languages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document_Types',
            fields=[
                ('document_type_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('document_type_name', models.CharField(max_length=155)),
            ],
            options={
                'db_table': 'Document_Types',
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('document_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('document_name', models.CharField(max_length=155)),
                ('document_date', models.DateField(auto_now_add=True)),
                ('document_unique_code', models.CharField(max_length=155, unique=True)),
                ('document_file', models.FileField(upload_to='uploads/')),
                ('document_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinak_app.document_types')),
            ],
            options={
                'db_table': 'Documents',
            },
        ),
    ]
