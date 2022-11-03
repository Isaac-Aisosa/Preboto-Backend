# Generated by Django 4.0 on 2022-04-11 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0003_revenuehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.BigIntegerField(default=0)),
                ('account', models.CharField(blank=True, max_length=225, null=True)),
                ('Recipient_account', models.CharField(blank=True, max_length=225, null=True)),
                ('terminalUser', models.CharField(blank=True, max_length=225, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
            ],
        ),
    ]