# Generated by Django 3.2.7 on 2021-11-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NM', '0010_wsc3650_max_fail'),
    ]

    operations = [
        migrations.AddField(
            model_name='wsc3650',
            name='stp_mode',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]