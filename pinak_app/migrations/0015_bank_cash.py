# Generated by Django 5.1.3 on 2024-12-18 15:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinak_app', '0014_bank_details_company_bank_account_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='bank_cash',
            fields=[
                ('bank_cash_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('credit_debit', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('details', models.TextField(blank=True, null=True)),
                ('bank_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinak_app.bank_details')),
            ],
            options={
                'db_table': 'bank_cash',
            },
        ),
    ]