# Generated by Django 5.1.3 on 2024-12-23 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinak_app', '0007_merge_20241223_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_investor',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='project_investor_fixed_amount',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='project_investor_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investor_name', to='pinak_app.person'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_investor_percentage',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='project_investor_type',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
        migrations.AlterField(
            model_name='project_material_data',
            name='project_material_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]