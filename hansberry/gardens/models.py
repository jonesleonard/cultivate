from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField
from localflavor.us.models import USZipCodeField
from localflavor.us.models import USPS_CHOICES
from localflavor.us.models import USPostalCodeField


# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating 'created'
    and 'modified' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Garden(TimeStampedModel):
    """
    Stores a single Garden entry, related to :model:'gardens.GardenAddress',
    :model:'gardens.GardenAddressType'
    """
    name = models.CharField('name', max_length=100)
    created_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(
        'slug of garden', unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify("{garden.name}-{garden.pk}".format(garden=self))
        super(Garden, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('garden-detail', kwargs={'pk': self.pk})


class GardenAddress(models.Model):
    """
    Stores a garden address entry tied to each garden, related to
    :model:'gardens.Garden', :model:'gardens.GardenAddressType',
    and :model:'gardens.ZipCode'
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
    garden = models.ForeignKey(
        Garden,
        on_delete=models.CASCADE,
        verbose_name='garden',
        null=True,
        blank=True
    )
    address = models.CharField('street address', max_length=50)
    city = models.CharField('city', max_length=100)
    state = USStateField('state', choices=STATE_CHOICES)
    zip_code = USZipCodeField('zip code')

    class Meta:
        ordering = ['address_type', 'city']

    def __str__(self):
        return '{}, {}, {} {}'.format(
            self.address, self.city, self.state, self.zip_code
        )


