# Generated by Django 2.0.2 on 2018-03-03 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0013_garden_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garden',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gardens.GardenAddress', verbose_name='the related garden address'),
        ),
    ]
