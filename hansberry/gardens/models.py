from django.db import models


# Create your models here.
class GardenAddressType(models.Model):
    ADDRESS_PHYSICAL = 'py'
    ADDRESS_MAILING = 'ml'

    ADDRESS_CHOICES = (
        (ADDRESS_PHYSICAL, 'Physical'),
        (ADDRESS_MAILING, 'Mailing')
    )

    address_type = models.CharField(
        'type of address',
        max_length=2,
        choices=ADDRESS_CHOICES,
        default=ADDRESS_PHYSICAL
    )


class State(models.Model):
    short_name = models.CharField('state short name', max_length=2, primary_key=True)
    name = models.CharField('state full name', max_length=50)


class City(models.Model):
    name = models.CharField('city name', max_length=100)
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        verbose_name='the related state',
    )


class ZipCode(models.Model):
    code = models.CharField('zip code', max_length=6)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='the related city',
    )


class GardenAddress(models.Model):
    address_type = models.ForeignKey(
        GardenAddressType,
        on_delete=models.CASCADE,
        verbose_name='the related address type',
    )
    address = models.CharField('street address', max_length=255, blank=True)
    zip_code = models.ForeignKey(
        ZipCode,
        on_delete=models.CASCADE,
        verbose_name='the related zip code',
    )


class Garden(models.Model):
    name = models.CharField('name of garden', max_length=100)
    slug = models.SlugField(max_length=40)
    address = models.ForeignKey(
        GardenAddress,
        on_delete=models.CASCADE,
        verbose_name='the related garden address',
    )