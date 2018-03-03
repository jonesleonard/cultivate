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

        # create more test gardens
        self.test_garden = Garden.objects.create(name='Test Garden')
        self.test_garden_2 = Garden.objects.create(name='Test Garden 2')
        self.test_garden_3 = Garden.objects.create(name='Test Garden 3')

    def test_view_url_accessible_by_name(self):
        """Tests that garden user can login"""
        login = self.client.login(username='testuser', password='secret')
        url = reverse('my-gardens')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # check if user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser')

    def test_redirect_if_not_logged_in(self):
        """Test that user is redirected to login page"""
        test_garden = self.hansberry_garden
        url = reverse('my-gardens')
        resp = self.client.get(url)
        self.assertRedirects(resp, '/accounts/login/?next=/mygardens/')

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser', password='secret')
        test_garden = self.hansberry_garden
        url = reverse('my-gardens')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # check if user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser')
        # check its using the correct template
        self.assertTemplateUsed(resp, 'gardens/gardens_list_user.html')

    def test_lists_user_garden(self):
        # test all user's gardens are listed
        login = self.client.login(username='testuser', password='secret')
        test_garden = self.hansberry_garden
        # associate user with garden
        test_garden.garden_author = User.objects.get(username='testuser')
        test_garden.save()
        url = reverse('my-gardens')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['object_list']), 1)

    def test_lists_multiple_user_gardens(self):
        # test all user's gardens are listed
        login = self.client.login(username='testuser', password='secret')
        # associate user with multiple gardens
        test_gardens = (self.test_garden, self.test_garden_2,
                        self.test_garden_3)
        for garden in test_gardens:
            garden.garden_author = User.objects.get(username='testuser')
            garden.save()
        url = reverse('my-gardens')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['object_list']), 3)


class GardenDetailViewTest(TestCase):
    def setUp(self):
        # create credentials
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
        }
        # create user
        User.objects.create_user(**self.credentials)

        # create garden with address
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
            address=self.gardenaddress_hansberry,
            description='great garden and delicious veggies')

    def test_view_url_accessible_by_name(self):
        url = reverse('garden-detail', args=(self.hansberry_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('garden-detail', args=(self.hansberry_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'gardens/garden_detail.html')

    def test_view_returns_garden_name(self):
        url = reverse('garden-detail', args=(self.hansberry_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.hansberry_garden.name)
    
    def test_view_returns_garden_description(self):
        url = reverse('garden-detail', args=(self.hansberry_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.hansberry_garden.description)

    def test_view_returns_garden_address(self):
        url = reverse('garden-detail', args=(self.hansberry_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.hansberry_garden.address)

    def test_view_returns_garden_404(self):
        url = reverse('garden-detail', args=(self.hansberry_garden.pk+1,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_view_returns_no_description_msg(self):
        test_garden = Garden.objects.create(name='Test Garden')
        url = reverse('garden-detail', args=(test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'This garden doesn\'t have a description yet.')

    def test_view_returns_no_address_msg(self):
        test_garden = Garden.objects.create(name='Test Garden')
        url = reverse('garden-detail', args=(test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'This garden doesn\'t have an address yet.')

    def test_view_no_address_has_description(self):
        test_garden = Garden.objects.create(name='Test Garden', description='test description')
        url = reverse('garden-detail', args=(test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, test_garden.description)
        self.assertContains(resp, 'This garden doesn\'t have an address yet.')
        self.assertNotContains(resp, 'This garden doesn\'t have a description yet.')

    def test_view_no_description_has_address(self):
        test_garden = Garden.objects.create(name='Test Garden', address=self.gardenaddress_hansberry)
        url = reverse('garden-detail', args=(test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, test_garden.address)
        self.assertContains(resp, 'This garden doesn\'t have a description yet.')
        self.assertNotContains(resp, 'This garden doesn\'t have an address yet.')

    def test_view_displays_name(self):
        test_garden = Garden.objects.create(name='Test Garden')
        url = reverse('garden-detail', args=(test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, test_garden.name)

    def test_view_displays_owner(self):
        test_garden = Garden.objects.create(name='Test Garden')
        test_garden.garden_author = User.objects.get(username='testuser')
        test_garden.save()
        url = reverse('garden-detail', args=(test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, test_garden.garden_author)


    


