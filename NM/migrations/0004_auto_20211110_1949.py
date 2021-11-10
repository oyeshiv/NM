# Generated by Django 3.2.7 on 2021-11-10 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NM', '0003_auto_20211110_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='isr4321',
            name='crypto_permit_end_wild',
            field=models.GenericIPAddressField(default='0.0.0.0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='isr4321',
            name='crypto_permit_ip_end',
            field=models.GenericIPAddressField(default='0.0.0.0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='isr4321',
            name='crypto_permit_ip_start',
            field=models.GenericIPAddressField(default='0.0.0.0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='isr4321',
            name='crypto_permit_start_wild',
            field=models.GenericIPAddressField(default='0.0.0.0'),
            preserve_default=False,
        ),
    ]