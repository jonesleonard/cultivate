from django.test import TestCase
from hansberry.gardens.models import *


class GardenTestCase(TestCase):
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
                                                                 slug='hgnc',
                                                                 address=self.gardenaddress_hansberry)
    def test_garden_name_label(self):
        field_label = self.hansberry_garden._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name of garden')


    def test_garden_address_label(self):
        field_label = self.hansberry_garden._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'the related garden address')

    def test_slug_field(self):
        

    def test_garden_name(self):
        self.assertEqual(self.hansberry_garden.name, 'Hansberry Garden and Nature Center')
