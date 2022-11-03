# Generated by Django 4.0 on 2022-04-07 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrebotoConstant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prebotoGainPercent', models.IntegerField(default=0)),
                ('prebotoLossPercent', models.IntegerField(default=0)),
                ('clientsGainPercent', models.IntegerField(default=0)),
                ('clientsLossPercent', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DailyTrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputAmount', models.BigIntegerField(default=0)),
                ('outputAmount', models.BigIntegerField(blank=True, default=0, null=True)),
                ('returns', models.BigIntegerField(blank=True, default=0, null=True)),
                ('terminal', models.CharField(blank=True, max_length=225, null=True)),
                ('tradeName', models.CharField(blank=True, max_length=225, null=True)),
                ('opened', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('gain', models.BooleanField(default=False)),
                ('loss', models.BooleanField(default=False)),
                ('openTime', models.TimeField(auto_now_add=True, verbose_name='openTime')),
                ('closeTime', models.TimeField(blank=True, null=True, verbose_name='closeTime')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('terminalUser', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='terminal', to='auth.user')),
            ],
        ),
    ]
