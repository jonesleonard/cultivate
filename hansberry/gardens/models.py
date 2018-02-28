from django.db import models
from django.template.defaultfilters import slugify


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

    def __str__(self):
        return self.ADDRESS_CHOICES


class State(models.Model):
    short_name = models.CharField('state short name', max_length=2, primary_key=True)
    name = models.CharField('state full name', max_length=50)

    def __str__(self):
        return self.name.upper()


class City(models.Model):
    name = models.CharField('city name', max_length=100)
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        verbose_name='the related state',
    )

    def __str__(self):
        return self.name


class ZipCode(models.Model):
    code = models.CharField('zip code', max_length=6)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='the related city',
    )

    def __str__(self):
        return self.code


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

    def __str__(self):
        return '%s, %s, %s %s'.format(self.address, self.zip_code.city, self.zip_code.city.state, self.zip_code)


class Garden(models.Model):
    name = models.CharField('name of garden', max_length=100)
    slug = models.SlugField()
    address = models.ForeignKey(
        GardenAddress,
        on_delete=models.CASCADE,
        verbose_name='the related garden address',
    )

    class Meta:
        unique_together = (('address', 'name'),)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Garden, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
