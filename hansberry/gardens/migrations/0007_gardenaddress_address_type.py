# Generated by Django 2.0.2 on 2018-03-04 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0006_auto_20180304_0248'),
    ]

    operations = [
        migrations.AddField(
            model_name='gardenaddress',
            name='address_type',
            field=models.CharField(choices=[('py', 'Physical'), ('ml', 'Mailing')], default='py', max_length=2, verbose_name='type of address'),
        ),
    ]
