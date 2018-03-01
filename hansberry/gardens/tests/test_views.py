from django.test import TestCase, TransactionTestCase

from hansberry.gardens.models import (Garden, GardenAddress, GardenAddressType,
                                      State, City, ZipCode)
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime


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
