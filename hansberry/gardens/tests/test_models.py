from django.test import TestCase
from django.db import IntegrityError

from hansberry.gardens.models import (Garden, GardenAddressType, GardenAddress, State, ZipCode, City)


class GardenModelTest(TestCase):
    def setUp(self):
        self.state_pa, created = State.objects.get_or_create(short_name='PA', name='Pennsylvania')
        self.city_philly, created = City.objects.get_or_create(name='Philadelphia', state=self.state_pa)
        self.zip_germantown, created = ZipCode.objects.get_or_create(code='19144', city=self.city_philly)
        self.gardenaddresstype_py, created = GardenAddressType.objects.get_or_create(address_type='py')
        self.gardenaddress_hansberry, created = GardenAddress.objects.get_or_create(
            address_type=self.gardenaddresstype_py,
            address='5150 Wayne Avenue',
            zip_code=self.zip_germantown)
        self.hansberry_garden, created = Garden.objects.get_or_create(name='Hansberry Garden and Nature Center',
                                                                 address=self.gardenaddress_hansberry)

    def test_garden_name_label(self):
        """A Garden's name label returns the correct verbose name"""
        field_label = self.hansberry_garden._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name of garden')

    def test_garden_address_label(self):
        """A Garden's address label returns teh correct verbose name"""
        field_label = self.hansberry_garden._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'the related garden address')

    def test_slug_field(self):
        """A Garden's slug field is correctly slugified"""
        self.assertEquals(self.hansberry_garden.slug, 'hansberry-garden-and-nature-center')

    def test_calling_garden_returns_its_name(self):
        """The str method in Garden returns the Garden's name"""
        name = self.hansberry_garden.name
        self.assertEquals(str(self.hansberry_garden), name)

    def test_name_max_length(self):
        """That the max_length of Garden is correctly returned"""
        max_length = self.hansberry_garden._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_unique_togther(self):
        """Ensure a garden with the same name and address can't be created twice"""
        with self.assertRaises(IntegrityError):
            Garden.objects.create(name='Hansberry Garden and Nature Center',
                                  address=self.gardenaddress_hansberry)


class GardenAddressModel(TestCase):
    def setUp(self):
        self.state_pa, created = State.objects.get_or_create(short_name='PA', name='Pennsylvania')
        self.city_philly, created = City.objects.get_or_create(name='Philadelphia', state=self.state_pa)
        self.zip_germantown, created = ZipCode.objects.get_or_create(code='19144', city=self.city_philly)
        self.gardenaddresstype_py, created = GardenAddressType.objects.get_or_create(address_type='py')
        self.gardenaddress_hansberry, created = GardenAddress.objects.get_or_create(
            address_type=self.gardenaddresstype_py,
            address='5150 Wayne Avenue',
            zip_code=self.zip_germantown)
        self.hansberry_garden, created = Garden.objects.get_or_create(name='Hansberry Garden and Nature Center',
                                                                      address=self.gardenaddress_hansberry)

    def test_gardenaddress_type_label(self):
        """A Garden's Address returns the correct verbose name for address_type"""
        gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
        field_label = gardenaddress._meta.get_field('address_type').verbose_name
        self.assertEquals(field_label, 'the related address type')

    def test_address_label(self):
        """Address field in GardenAddress returns correct verbose name"""
        gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
        field_label = gardenaddress._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'street address')

    def test_gardenaddress_zip_label(self):
        """Tests zip label"""
        gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
        field_label = gardenaddress._meta.get_field('zip_code').verbose_name
        self.assertEquals(field_label, 'the related zip code')

    def test_calling_gardenaddress_returns_formmattedd_address(self):
        """GardenAddress str method returns correctly formatted address"""
        gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
        formatted_address = '%s, %s, %s %s'.format(gardenaddress.address, self.city_philly, self.state_pa, self.zip_germantown)
        self.assertEquals(str(gardenaddress), formatted_address)

    def test_address_max_length(self):
        """GardenAddress address field returns the correct max length"""
        gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
        max_length = gardenaddress._meta.get_field('address').max_length
        self.assertEquals(max_length, 255)
