# Generated by Django 4.0 on 2022-04-23 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer_Care', '0002_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppDownloadLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playStore', models.CharField(blank=True, max_length=225, null=True)),
                ('AppStore', models.CharField(blank=True, max_length=225, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]