from django.test import TestCase
from django.urls import resolve
from django. http import HttpRequest

from lists.views import home_page
from lists.models import Item, List

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_after_POST_request_(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')



class ListViewTests(TestCase):
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        wrong_list = List.objects.create()
        Item.objects.create(text='item 1', list = correct_list)
        Item.objects.create(text='item 2', list = correct_list)
        Item.objects.create(text='wrong item 3', list = wrong_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'wrong item 3')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        ## f notation is python string formatting
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class PostViewTests(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new',
            data={
            'item_text': 'A new list item'
            })

        #Make sure it saved the item to the database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new',
            data={'item_text': 'A new list item'})
        new_list = List.objects.first()

        self.assertRedirects(response, f'/lists/{new_list.id}/')

class HomePageTests(TestCase):

    def test_home_page_returns_correct_html_uses_home_template(self):
        #use Django Test Client to call the view we want by passing a URL
        response = self.client.get('/')
        #This allows us to check which template was used to render a response
        self.assertTemplateUsed(response, 'lists/home.html')

class ListAndItemModelsTests(TestCase):

    def test_saving_and_retrieving_items_from_1_list(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'first ever list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'second item text'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'first ever list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'second item text')
        self.assertEqual(second_saved_item.list, list_)
