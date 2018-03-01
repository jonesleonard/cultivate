from django.test import TestCase
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage


class TestStaticFiles(TestCase):
    """Check if gardens contains required css static files"""
    def test_gardens_css(self):
        abs_path = finders.find('gardens/css/main.css')
        print(abs_path)
        self.assertTrue(staticfiles_storage.exists(abs_path))

    def test_gardens_static(self):
        abs_path = finders.find('gardens/main.css')
        searched_locations = finders.searched_locations
        print(finders.searched_locations)
        self.assertEquals(searched_locations, abs_path)

