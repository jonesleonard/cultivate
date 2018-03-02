from django.test import TestCase, TransactionTestCase

from hansberry.gardens.models import (Garden, GardenAddress, GardenAddressType,
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


class GardenListView(TestCase):

    def setUp(self):
        # create test users
        test_user1 = User.objects.create_user(username='testuser1',
                                              password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2',
                                              password='12345')
        test_user2.save()

        # create garden
        self.state_pa, created = State.objects.get_or_create(
            short_name='PA', name='Pennsylvania')
        self.city_philly, created = City.objects.get_or_create(
            name='Philadelphia', state=self.state_pa)
        self.zip_germantown, created = ZipCode.objects.get_or_create(
            code='19144', city=self.city_philly)
        self.gardenaddresstype_py, created =
        GardenAddressType.objects.get_or_create(address_type='py')
        self.gardenaddress_hansberry, created =
        GardenAddress.objects.get_or_create(
            address_type=self.gardenaddresstype_py,
            address='5150 Wayne Avenue',
            zip_code=self.zip_germantown)
        self.hansberry_garden, created = Garden.objects.get_or_create(
            name='Hansberry Garden and Nature Center',
            address=self.gardenaddress_hansberry)
        self.hansberry_garden.save()

    def test_view_url_accessible_by_name(self):
        """Tests that garden user can login"""
        resp = self.client.login(username='testuser1', password='12345')

        self.assertEqual(resp.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        """Tests that garden list is returned at correct url"""
        resp = self.c.post('/accounts/login/',
                           {'username': 'garden_member_user',
                            'password': 'password123',
                            '?next': '/mygardens/'})
        resp = self.client.get('/mygardens/')
        print(resp)
        self.assertEquals(resp.status_code, 200)
