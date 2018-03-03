from django.test import TestCase, TransactionTestCase

from hansberry.gardens.models import (Garden,
                                      GardenAddress, GardenAddressType,
                                      State, City, ZipCode)
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime
from django.test import Client


class IndexViewTests(TestCase):

    def test_view_url_exists_at_desired_location(self):
        """Tests that index is at root url"""
        resp = self.client.get('/')
        self.assertEquals(resp.status_code, 200)

    def test_view_accessible_by_name(self):
        """Tests that Index is accessible by name"""
        resp = self.client.get(reverse('index'))
        self.assertEquals(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        """Tests that index uses the correct template"""
        resp = self.client.get(reverse('index'))
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'gardens/index.html')


class GardenOwnerListViewTest(TestCase):

    def setUp(self):
        # create credentials
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        # create test user
        User.objects.create_user(**self.credentials)

        # create garden
        self.state_pa, created = State.objects.get_or_create(
            short_name='PA', name='Pennsylvania')
        self.city_philly, created = City.objects.get_or_create(
            name='Philadelphia', state=self.state_pa)
        self.zip_germantown, created = ZipCode.objects.get_or_create(
            code='19144', city=self.city_philly)
        self.gardenaddresstype_py, created = GardenAddressType.objects.get_or_create(
            address_type='py')
        self.gardenaddress_hansberry, created = GardenAddress.objects.get_or_create(
            address_type=self.gardenaddresstype_py,
            address='5150 Wayne Avenue',
            zip_code=self.zip_germantown
        )
        self.hansberry_garden, created = Garden.objects.get_or_create(
            name='Hansberry Garden and Nature Center',
            address=self.gardenaddress_hansberry)

    def test_login(self):
        """Tests that garden user can login"""
        login = self.client.login(username='testuser', password='secret')
        url = reverse('my-gardens')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # check if user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser')
