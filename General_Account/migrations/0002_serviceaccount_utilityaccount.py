# Generated by Django 4.0 on 2022-04-09 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('General_Account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceAccount',
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
            name='UtilityAccount',
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
