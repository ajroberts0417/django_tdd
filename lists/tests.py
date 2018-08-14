from django.test import TestCase
from django.urls import resolve
from django. http import HttpRequest

from lists.views import home_page


class HomePageTests(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        #use Django Test Client to call the view we want by passing a URL
        response = self.client.get('/')

        #This allows us to check which template was used to render a response
        self.assertTemplateUsed(response, 'home.html')
