# Generated by Django 3.2.7 on 2021-11-26 17:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('NM', '0035_alter_scripts_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scripts',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 26, 17, 49, 47, 511036, tzinfo=utc)),
        ),
    ]