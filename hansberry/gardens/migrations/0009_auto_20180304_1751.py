# Generated by Django 2.0.2 on 2018-03-04 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0008_auto_20180304_0306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garden',
            name='address',
        ),
        migrations.AddField(
            model_name='gardenaddress',
            name='garden',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gardens.Garden', verbose_name='garden'),
        ),
    ]
