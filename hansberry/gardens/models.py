from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify


# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating 'created' and 'modified' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GardenAddressType(models.Model):
    """
    Stores the type of address a garden address entry is, related to :model:'gardens.GardenAddress' and
    :model:'gardens.Garden',
    """
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
        return self.get_address_type_display()


class State(models.Model):
    """
    Stores a single US State entry
    """
    short_name = models.CharField('state short name', max_length=2, primary_key=True)
    name = models.CharField('state full name', max_length=50)

    def save(self, *args, **kwargs):
        self.short_name = self.short_name.upper()
        self.name = self.name.title()
        super(State, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Stores a single US City entry, related to :model:'gardens.State'
    """
    name = models.CharField('city name', max_length=100)
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        verbose_name='the related state',
    )

    def __str__(self):
        return self.name


class ZipCode(models.Model):
    """
    Stores zip code data, related to :model:'gardens.city'
    """
    code = models.CharField('zip code', max_length=6)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='the related city',
    )

    class Meta:
        unique_together = (('code', 'city'),)

    def __str__(self):
        return self.code


class GardenAddress(models.Model):
    """
    Stores a garden address entry tied to each garden, related to :model:'gardens.Garden',
    :model:'gardens.GardenAddressType', and :model:'gardens.ZipCode'
    """
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
        return '{}, {}, {} {}'.format(self.address, self.zip_code.city, self.zip_code.city.state, self.zip_code)


class Garden(TimeStampedModel):
    """
    Stores a single Garden entry, related to :model:'gardens.GardenAddress',
    :model:'gardens.GardenAddressType'
    """
    garden_author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.CharField(max_length=300, null=True)
    name = models.CharField('name of garden', max_length=100)
    slug = models.SlugField('slug of garden', unique=True, blank=True, null=True)
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
