# Generated by Django 3.2.7 on 2021-11-26 17:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('NM', '0036_alter_scripts_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scripts',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
