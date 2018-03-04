from django.test import TestCase
from django.db import IntegrityError

from hansberry.gardens.models import (
    Garden, GardenAddressType, GardenAddress)


# class GardenModelTest(TestCase):
#     def setUp(self):
#         self.state_pa = State.objects.create(
#             short_name='PA', name='Pennsylvania')
#         self.city_philly = City.objects.create(
#             name='Philadelphia', state=self.state_pa)
#         self.zip_germantown = ZipCode.objects.create(
#             code='19144', city=self.city_philly)
#         self.gardenaddresstype_py = GardenAddressType.objects.create(
#             address_type='py')
#         self.gardenaddress_hansberry = GardenAddress.objects.create(
#             address_type=self.gardenaddresstype_py,
#             address='5150 Wayne Avenue',
#             zip_code=self.zip_germantown)
#         self.hansberry_garden = Garden.objects.create(
#             name='Hansberry Garden and Nature Center',
#             address=self.gardenaddress_hansberry)

#     def test_garden_name_label(self):
#         """A Garden's name label returns the correct verbose name"""
#         field_label = self.hansberry_garden._meta.get_field(
#             'name').verbose_name
#         self.assertEquals(field_label, 'name of garden')

#     def test_garden_address_label(self):
#         """A Garden's address label returns teh correct verbose name"""
#         field_label = self.hansberry_garden._meta.get_field(
#             'address').verbose_name
#         self.assertEquals(field_label, 'the related garden address')

#     def test_slug_field(self):
#         """A Garden's slug field is correctly slugified"""
#         self.assertEquals(self.hansberry_garden.slug,
#                           'hansberry-garden-and-nature-center')

#     def test_calling_garden_returns_its_name(self):
#         """The str method in Garden returns the Garden's name"""
#         name = self.hansberry_garden.name
#         self.assertEquals(str(self.hansberry_garden), name)

#     def test_name_max_length(self):
#         """That the max_length of Garden is correctly returned"""
#         max_length = self.hansberry_garden._meta.get_field('name').max_length
#         self.assertEquals(max_length, 100)

#     def test_unique_togther(self):
#         """Ensure a garden with the same name and address can't be created twice"""
#         with self.assertRaises(IntegrityError):
#             Garden.objects.create(name='Hansberry Garden and Nature Center',
#                                   address=self.gardenaddress_hansberry)


# class GardenAddressModel(TestCase):
#     def setUp(self):
#         state_pa = State.objects.create(short_name='PA', name='Pennsylvania')
#         city_philly = City.objects.create(
#             name='Philadelphia', state=state_pa)
#         zip_germantown = ZipCode.objects.create(
#             code='19144', city=city_philly)
#         gardenaddresstype_py = GardenAddressType.objects.create(
#             address_type='py')
#         gardenaddress_hansberry = GardenAddress.objects.create(
#             address_type=gardenaddresstype_py,
#             address='5150 Wayne Avenue',
#             zip_code=zip_germantown)
#         hansberry_garden = Garden.objects.create(
#             name='Hansberry Garden and Nature Center',
#             address=gardenaddress_hansberry
#         )

#     def test_gardenaddress_type_label(self):
#         """Garden's Address returns the correct verbose name for address_type"""
#         gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
#         field_label = gardenaddress._meta.get_field(
#             'address_type').verbose_name
#         self.assertEquals(field_label, 'the related address type')

#     def test_address_label(self):
#         """Address field in GardenAddress returns correct verbose name"""
#         gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
#         field_label = gardenaddress._meta.get_field('address').verbose_name
#         self.assertEquals(field_label, 'street address')

#     def test_gardenaddress_zip_label(self):
#         """Tests zip label"""
#         gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
#         field_label = gardenaddress._meta.get_field('zip_code').verbose_name
#         self.assertEquals(field_label, 'the related zip code')

#     def test_calling_gardenaddress_returns_formmattedd_address(self):
#         """GardenAddress str method returns correctly formatted address"""
#         gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
#         city_philly = City.objects.get(name='Philadelphia')
#         state_pa = State.objects.get(short_name='PA')
#         zip_germantown = ZipCode.objects.get(code='19144')
#         formatted_address = '{}, {}, {} {}'.format(gardenaddress.address,
#                                                    city_philly, state_pa,
#                                                    zip_germantown)
#         self.assertEquals(str(gardenaddress), formatted_address)

#     def test_address_max_length(self):
#         """GardenAddress address field returns the correct max length"""
#         gardenaddress = GardenAddress.objects.get(address='5150 Wayne Avenue')
#         max_length = gardenaddress._meta.get_field('address').max_length
#         self.assertEquals(max_length, 255)


# class ZipCodeModel(TestCase):
#     def setUp(self):
#         self.state_pa, created = State.objects.get_or_create(
#             short_name='PA', name='Pennsylvania')
#         self.city_philly, created = City.objects.get_or_create(
#             name='Philadelphia', state=self.state_pa)
#         self.zip_germantown, created = ZipCode.objects.get_or_create(
#             code='19144', city=self.city_philly)

#     def test_code_label(self):
#         """Test that the correct verbose name is returned"""
#         test_zip = ZipCode.objects.get(code='19144')
#         field_label = test_zip._meta.get_field('code').verbose_name
#         self.assertEquals(field_label, 'zip code')

#     def test_code_max_length(self):
#         """Test that the correct max length is returned"""
#         test_zip = ZipCode.objects.get(code='19144')
#         max_length = test_zip._meta.get_field('code').max_length
#         self.assertEquals(max_length, 6)

#     def test_calling_zip_returns_its_code(self):
#         """Test that ZipCode's str method returns the zip code"""
#         test_zip = ZipCode.objects.get(code='19144')
#         zip_code = test_zip.code
#         self.assertEquals(str(test_zip), zip_code)

#     def test_city_label(self):
#         test_zip = ZipCode.objects.get(code='19144')
#         field_label = test_zip._meta.get_field('city').verbose_name
#         self.assertEquals(field_label, 'the related city')

#     def test_unique_together(self):
#         """Test that a zip code can't have more than one city"""
#         with self.assertRaises(IntegrityError):
#             ZipCode.objects.create(code='19144', city=self.city_philly)

#     def test_ok_to_create_zip_in_existing_city(self):
#         """Test that a new zip can be created in an existing city"""
#         test_zip_diff, created = ZipCode.objects.get_or_create(
#             code='19154', city=self.city_philly)
#         self.assertEquals(created, 1)

#     def test_new_zip_same_city(self):
#         """Test the name field of a newly created zip in an existing city"""
#         test_zip_diff, created = ZipCode.objects.get_or_create(
#             code='19164', city=self.city_philly)
#         self.assertEquals(test_zip_diff.city.name, 'Philadelphia')


# class CityModel(TestCase):
#     def setUp(self):
#         self.state_pa, created = State.objects.get_or_create(
#             short_name='PA', name='Pennsylvania')
#         self.city_philly, created = City.objects.get_or_create(
#             name='Philadelphia', state=self.state_pa)

#     def test_name_str(self):
#         """Test the str method for the correct name"""
#         city = City.objects.get(name='Philadelphia')
#         self.assertEquals(str(city), city.name)

#     def test_name_label(self):
#         """Test that the correct verbose name is returned"""
#         city = City.objects.get(name='Philadelphia')
#         field_label = city._meta.get_field('name').verbose_name
#         self.assertEquals(field_label, 'city name')

#     def test_name_max_length(self):
#         """Test that the correct max length is returned"""
#         city = City.objects.get(name='Philadelphia')
#         max_length = city._meta.get_field('name').max_length
#         self.assertEquals(max_length, 100)

#     def test_state_label(self):
#         """Test that the correct label for the state field is returned"""
#         city = City.objects.get(name='Philadelphia')
#         field_label = city._meta.get_field('state').verbose_name
#         self.assertEquals(field_label, 'the related state')


# class StateModel(TestCase):
#     def setUp(self):
#         self.state_pa, created = State.objects.get_or_create(
#             short_name='PA', name='Pennsylvania')

#     def test_state_str(self):
#         """Test str method of State model"""
#         test_state = State.objects.get(short_name='PA')
#         self.assertEquals(str(test_state), test_state.name)

#     def test_short_name_label(self):
#         """Test short_name field returns correct verbose name"""
#         test_state = State.objects.get(short_name='PA')
#         field_label = test_state._meta.get_field('short_name').verbose_name
#         self.assertEquals(field_label, 'state short name')

#     def test_short_name_max_length(self):
#         """Test short_name field returns correct max length"""
#         test_state = State.objects.get(short_name='PA')
#         max_length = test_state._meta.get_field('short_name').max_length
#         self.assertEquals(max_length, 2)

#     def test_name_label(self):
#         """Test name label returns correct verbose name"""
#         test_state = State.objects.get(short_name='PA')
#         field_label = test_state._meta.get_field('name').verbose_name
#         self.assertEquals(field_label, 'state full name')

#     def test_name_label_max_length(self):
#         """Test name label returns correct max length"""
#         test_state = State.objects.get(short_name='PA')
#         max_length = test_state._meta.get_field('name').max_length
#         self.assertEquals(max_length, 50)

#     def test_short_name_upper(self):
#         """Test short_name is saved in uppercase"""
#         test_state, created = State.objects.get_or_create(
#             short_name='nj', name='New Jersey')
#         self.assertEquals(test_state.short_name, 'NJ')

#     def test_name_title(self):
#         """Test that name field is saved with each word capitalized"""
#         test_state, created = State.objects.get_or_create(
#             short_name='NJ', name='new jersey')
#         self.assertEquals(test_state.name, 'New Jersey')


# class GardenAddressTypeModel(TestCase):
#     def setUp(self):
#         self.gardenaddresstype_py, created = GardenAddressType.objects.get_or_create(
#             address_type='py')
#         self.gardenaddresstype_py, created = GardenAddressType.objects.get_or_create(
#             address_type='ml')

#     def test_garden_type_choices_count(self):
#         """Test the length of the choices"""
#         num_of_address_types = len(GardenAddressType.ADDRESS_CHOICES)
#         self.assertEquals(num_of_address_types, 2)

#     def test_garden_address_type_physical_str(self):
#         """Test that the str method returns Physical for py"""
#         test_garden_address_type = GardenAddressType.objects.get(
#             address_type='py')
#         self.assertEquals(str(test_garden_address_type), 'Physical')

#     def test_garden_address_type_physical_str(self):
#         """Test that the str method returns Mailing for ml"""
#         test_garden_address_type = GardenAddressType.objects.get(
#             address_type='ml')
#         self.assertEquals(str(test_garden_address_type), 'Mailing')

#     def test_address_type_label(self):
#         """Test that the label for address_type returns the correct verbose name"""
#         test_garden_address_type = GardenAddressType.objects.get(
#             address_type='py')
#         field_label = test_garden_address_type._meta.get_field(
#             'address_type').verbose_name
#         self.assertEquals(field_label, 'type of address')

#     def test_address_type_max_length(self):
#         """Test that the max_length on the address type field is correct"""
#         test_garden_address_type = GardenAddressType.objects.get(
#             address_type='py')
#         max_length = test_garden_address_type._meta.get_field(
#             'address_type').max_length
#         self.assertEquals(max_length, 2)
