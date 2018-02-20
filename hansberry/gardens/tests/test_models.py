from django.test import TestCase
from hansberry.gardens.models import *


class GardenTestCase(TestCase):
    def setUp(self):
        State.objects.get_or_create(short_name='PA', name='Pennsylvania')
        City.objects.get_or_create(name='Philadelphia', state__id=1)

    def test_city(self):
        state = State.objects.get_or_create(short_name='PA')
        city = City.objects.get_or_create(name='Philadelphia')
        self.assertEqual(city.name, 'Philadelphia')
        self.assertEqual(state.name, 'Pennsylvania')

