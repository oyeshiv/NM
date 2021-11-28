# Generated by Django 3.2.7 on 2021-11-28 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NM', '0038_c1000_interface_c1000_vlan_c1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acl_3650',
            name='script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NM.scripts'),
        ),
        migrations.AlterField(
            model_name='ciscouser',
            name='script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NM.scripts'),
        ),
        migrations.AlterField(
            model_name='interface_c1000',
            name='script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NM.c1000'),
        ),
        migrations.AlterField(
            model_name='vlan_c1000',
            name='script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NM.c1000'),
        ),
    ]
