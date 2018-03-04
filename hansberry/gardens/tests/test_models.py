from django.test import TestCase
from django.db import IntegrityError
from django.template.defaultfilters import slugify

from hansberry.gardens.models import (
    Garden, GardenAddress)


class GardenModelTest(TestCase):

    def setUp(self):
        self.garden = Garden.objects.create(
            name='test garden',
            description='this is a test garden'
        )

        self.address = GardenAddress.objects.create(
            address='13000 Main Street',
            city='Philadelphia',
            state='PA',
            zip_code='19144'
        )

    def test_garden_name_label(self):
        """A Garden's name label returns the correct verbose name"""
        field_label = self.garden._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_garden_address_label(self):
        """A Garden's address label returns teh correct verbose name"""
        field_label = self.garden._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_slug_field(self):
        """A Garden's slug field is correctly slugified"""
        self.assertEquals(self.garden.slug, 'test-garden')

    def test_calling_garden_returns_its_name(self):
        """The str method in Garden returns the Garden's name"""
        name = self.garden.name
        self.assertEquals(str(self.garden), name)

    def test_name_max_length(self):
        """That the max_length of Garden is correctly returned"""
        max_length = self.garden._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_unique_togther(self):
        """Ensure a garden with the same name and address can't be created twice"""
        # create another garden with same name and address
        with self.assertRaises(IntegrityError):
            Garden.objects.create(name='test garden', address=self.address)

    def test_get_absolute_url(self):
        # This will also fail if the urlconf is not defined.
        garden_pk = self.garden.pk
        self.assertEqual(self.garden.get_absolute_url(), '/{}'.format(garden_pk))

    def test_slug_field_save(self):
        garden_pk = self.garden.pk
        slugified_name = slugify(self.garden.name)
        formatted_slug = "{}-{}".format(slugified_name, garden_pk)
        self.garden.save()
        self.assertEqual(self.garden.slug, formatted_slug)


class GardenAddressModelTest(TestCase):

    def setUp(self):
        self.garden = Garden.objects.create(
            name='test garden',
            description='this is a test garden'
        )

        self.address = GardenAddress.objects.create(
            address='13000 Main Street',
            city='Philadelphia',
            state='PA',
            zip_code='19144'
        )

    def test_gardenaddress_type_label(self):
        """Garden's Address returns the correct verbose name for address_type"""
        field_label = self.address._meta.get_field('address_type').verbose_name
        self.assertEquals(field_label, 'type of address')

    def test_address_label(self):
        """Address field in GardenAddress returns correct verbose name"""
        field_label = self.address._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'street address')

    def test_gardenaddress_zip_label(self):
        """Tests zip label"""
        field_label = self.address._meta.get_field('zip_code').verbose_name
        self.assertEquals(field_label, 'zip code')

    def test_gardenaddress_city_label(self):
        """Tests city label"""
        field_label = self.address._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'city')

    def test_gardenaddress_state_label(self):
        """Tests state label"""
        field_label = self.address._meta.get_field('state').verbose_name
        self.assertEquals(field_label, 'state')

    def test_calling_gardenaddress_returns_formmattedd_address(self):
        """GardenAddress str method returns correctly formatted address"""
        formatted_address = '{}, {}, {} {}'.format(
            self.address.address, self.address.city,
            self.address.state, self.address.zip_code
        )
        self.assertEquals(str(self.address), formatted_address)

    def test_address_max_length(self):
        """GardenAddress address field returns the correct max length"""
        max_length = self.address._meta.get_field('address').max_length
        self.assertEquals(max_length, 50)

    def test_city_max_length(self):
        """GardenAddress city field returns the correct max length"""
        max_length = self.address._meta.get_field('city').max_length
        self.assertEquals(max_length, 100)

    def test_address_type_max_length(self):
        """GardenAddress address type field returns the correct max length"""
        max_length = self.address._meta.get_field('address_type').max_length
        self.assertEquals(max_length, 2)

    def test_garden_type_choices_count(self):
        """Test the length of the choices"""
        num_of_address_types = len(GardenAddress.ADDRESS_CHOICES)
        self.assertEquals(num_of_address_types, 2)

    def test_garden_address_type_physical(self):
        """Garden Address Physical"""
        test_garden_address_type = GardenAddress.ADDRESS_PHYSICAL
        self.assertEquals(test_garden_address_type, 'py')

    def test_garden_address_type_mailing(self):
        """Garden Address Mailing"""
        test_garden_address_type = GardenAddress.ADDRESS_MAILING
        self.assertEquals(test_garden_address_type, 'ml')

    def test_garden_address_type_physical(self):
        """Garden Address Physical"""
        self.assertTrue((GardenAddress.ADDRESS_PHYSICAL, 'Physical')
                        in GardenAddress.ADDRESS_CHOICES)

    def test_garden_address_type_mailing(self):
        """Garden Address Mailing"""
        self.assertTrue((GardenAddress.ADDRESS_MAILING, 'Mailing')
                        in GardenAddress.ADDRESS_CHOICES)
