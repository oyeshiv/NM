# Generated by Django 3.2.7 on 2021-11-18 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NM', '0002_rename_g00_ip_isr4321_g00_ipv4'),
    ]

    operations = [
        migrations.RenameField(
            model_name='isr4321',
            old_name='g01_ip',
            new_name='g01_ipv4',
        ),
    ]