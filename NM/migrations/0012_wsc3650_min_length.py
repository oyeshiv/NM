# Generated by Django 3.2.7 on 2021-11-24 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NM', '0011_wsc3650_stp_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='wsc3650',
            name='min_length',
            field=models.IntegerField(default=8),
            preserve_default=False,
        ),
    ]
