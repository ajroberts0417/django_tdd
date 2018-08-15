from django.test import TestCase
from django.urls import resolve
from django. http import HttpRequest

from lists.views import home_page
from lists.models import Item


class HomePageTests(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        #use Django Test Client to call the view we want by passing a URL
        response = self.client.get('/')

        #This allows us to check which template was used to render a response
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')


class ItemModelTests(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'first ever list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'second item text'
        second_item.save()

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'first ever list item')
        self.assertEqual(second_saved_item.text, 'second item text')
