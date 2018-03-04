from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime
from django.test import Client
from hansberry.gardens.models import Garden, GardenAddress
from hansberry.gardens.views import GardenOwnerListView


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

        # create test gardens
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
        url = reverse('my-gardens')
        resp = self.client.get(url)
        self.assertRedirects(resp, '/accounts/login/?next=/mygardens/')

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser', password='secret')
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
        # associate user with garden
        self.test_garden.created_by = User.objects.get(username='testuser')
        self.test_garden.save()
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
            garden.created_by = User.objects.get(username='testuser')
            garden.save()
        url = reverse('my-gardens')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['object_list']), 3)

    def test_paginate_number(self):
        login = self.client.login(username='testuser', password='secret')
        self.assertEqual(GardenOwnerListView.paginate_by, 10)


class GardenDetailViewTest(TestCase):
    def setUp(self):
        # create credentials
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
        }
        # create user
        User.objects.create_user(**self.credentials)

        # create test gardens
        self.test_garden = Garden.objects.create(name='Test Garden')
        # create test garden address
        self.test_garden_address = GardenAddress.objects.create(
            address='13000 Main Street',
            city='Philadelphia',
            state='PA',
            zip_code='19144'
        )

    def test_view_url_accessible_by_name(self):
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'gardens/garden_detail.html')

    def test_view_returns_garden_name(self):
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.test_garden.name)

    def test_view_returns_garden_description(self):
        self.test_garden.description = 'test description'
        self.test_garden.save()
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.test_garden.description)

    def test_view_returns_garden_address(self):
        self.test_garden.address = self.test_garden_address
        self.test_garden.save()
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.test_garden.address)

    def test_view_returns_garden_404(self):
        url = reverse('garden-detail', args=(self.test_garden.pk+1,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_view_returns_no_description_msg(self):
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(
            resp, 'This garden doesn\'t have a description yet.')

    def test_view_returns_no_address_msg(self):
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'This garden doesn\'t have an address yet.')

    def test_view_no_address_has_description(self):
        self.test_garden.description = 'this is a test description'
        self.test_garden.save()
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.test_garden.description)
        self.assertContains(resp, 'This garden doesn\'t have an address yet.')
        self.assertNotContains(
            resp, 'This garden doesn\'t have a description yet.')

    def test_view_no_description_has_address(self):
        self.test_garden.address = self.test_garden_address
        self.test_garden.save()
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.test_garden.address)
        self.assertContains(
            resp, 'This garden doesn\'t have a description yet.')
        self.assertNotContains(
            resp, 'This garden doesn\'t have an address yet.')

    def test_view_displays_name(self):
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.test_garden.name)

    def test_view_displays_owner(self):
        self.test_garden.created_by = User.objects.get(username='testuser')
        self.test_garden.save()
        url = reverse('garden-detail', args=(self.test_garden.pk,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.test_garden.created_by)


class GardenCreateViewTest(TestCase):
    def setUp(self):
        # create credentials
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
        }
        # create user
        User.objects.create_user(**self.credentials)

        # create test gardens
        self.test_garden = Garden.objects.create(name='Test Garden')
        # create test garden address
        self.test_garden_address = GardenAddress.objects.create(
            address='13000 Main Street',
            city='Philadelphia',
            state='PA',
            zip_code='19144'
        )
        self.test_garden.save()

    def test_redirect_if_not_logged_in(self):
        url = reverse('garden-create')
        resp = self.client.get(url)
        self.assertRedirects(resp, '/accounts/login/?next=/create/')

    def test_view_accessible_by_name(self):
        login = self.client.login(username='testuser', password='secret')
        url = reverse('garden-create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser', password='secret')
        url = reverse('garden-create')
        resp = self.client.get(url)
        self.assertTemplateUsed(resp, 'gardens/garden_form.html')

    def test_form_invalid_no_name(self):
        login = self.client.login(username='testuser', password='secret')
        url = reverse('garden-create')
        resp = self.client.post(url, {})
        self.assertFormError(resp, 'form', 'name', 'This field is required.')

    def test_form_invalid_when_same_name_and_address(self):
        login = self.client.login(username='testuser', password='secret')
        url = reverse('garden-create')
        resp = self.client.post(
            url,
            {'name': 'Test Garden', 'address': self.test_garden_address}
        )
        self.assertFormError(resp, 'form', 'address', 'Sorry, a garden with this name and address already exists.')
