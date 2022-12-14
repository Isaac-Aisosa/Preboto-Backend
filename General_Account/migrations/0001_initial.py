# Generated by Django 4.0 on 2022-04-07 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepositAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.BigIntegerField(default=0)),
                ('bank_account_number', models.CharField(blank=True, max_length=15, null=True)),
                ('bank_account_name', models.CharField(blank=True, max_length=225, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=225, null=True)),
                ('active', models.BooleanField(default=False)),
                ('block', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
            ],
        ),
        migrations.CreateModel(
            name='PrebotoWithdrawAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.BigIntegerField(default=0)),
                ('bank_account_number', models.CharField(blank=True, max_length=15, null=True)),
                ('bank_account_name', models.CharField(blank=True, max_length=225, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=225, null=True)),
                ('active', models.BooleanField(default=False)),
                ('block', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
            ],
        ),
        migrations.CreateModel(
            name='RevenueAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.BigIntegerField(default=0)),
                ('bank_account_number', models.CharField(blank=True, max_length=15, null=True)),
                ('bank_account_name', models.CharField(blank=True, max_length=225, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=225, null=True)),
                ('active', models.BooleanField(default=False)),
                ('block', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
            ],
        ),
    ]
