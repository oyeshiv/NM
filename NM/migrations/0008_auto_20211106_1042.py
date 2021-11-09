# Generated by Django 3.2.7 on 2021-11-06 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NM', '0007_auto_20211029_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='isr4321',
            name='ntp_trust_key',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='isr4321',
            name='tunnel_destination_address',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='isr4321',
            name='tunnel_protection_profile',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
