from django.test import TestCase
from hansberry.gardens.models import *


class GardenTestCase(TestCase):
    def setUp(self):
        self.state_pa, created = State.objects.get_or_create(short_name='PA', name='Pennsylvania')
        self.city_philly, created = City.objects.get_or_create(name='Philadelphia', state=state_pa)
        self.zip_germantown, created = ZipCode.objects.get_or_create(code='19144', city=city_philly)
        self.gardenaddresstype_py, created = GardenAddressType.objects.get_or_create(address_type='py')
        self.gardenaddress_hansberry, created = GardenAddress.objects.get_or_create(address_type=gardenaddresstype_py,
                                                                               address='5150 Wayne Avenue',
                                                                               zip_code=zip_germantown)

    def test_garden_name(self):
        hansberry_garden, created = Garden.objects.get_or_create(name='Hansberry Garden and Nature Center',
                                                        slug='hgnc',
                                                        address=self.gardenaddress_hansberry)
        self.assertEqual(hansberry_garden.name, 'Hansberry Garden and Nature Center')

