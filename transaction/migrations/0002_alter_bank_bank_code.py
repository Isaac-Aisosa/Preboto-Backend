# Generated by Django 4.0 on 2022-04-07 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='bank_code',
            field=models.IntegerField(default=0),
        ),
    ]
