# Generated by Django 2.0.2 on 2018-02-28 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0003_auto_20180228_2136'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='zipcode',
            unique_together={('code', 'city')},
        ),
    ]
