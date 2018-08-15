from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#make our test, inheriting from LiveServerTestCase (a django testing class)
class NewVisitorTest(LiveServerTestCase):

    # set up is always called at the beginning of the test
    def setUp(self):
        self.browser = webdriver.Firefox()

    # tearDown is always called at the end, even if the test fails
    def tearDown(self):
        self.browser.quit()

    def check_for_text_in_row_of_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # Helper function: adds any number of items to the to-do list
    # via the inputbox in the website, and returns the inputbox
    def input_items_into_to_do_list(self, *input_items):
        inputbox = self.browser.find_element_by_id('id_new_item')
        for item in input_items:
            inputbox.send_keys(item)
            inputbox.send_keys(Keys.ENTER)
            time.sleep(1)
        return inputbox

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Andrew was born to learn about a cool new online to-do app.
        # He goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Learn Django" into a text box (because he is a software developer)
        # When he hits ENTER, the page updates, and now it lists:
        # "1: Learn Django" as an item in a to-do list
        self.input_items_into_to_do_list('Learn Django')
        self.check_for_text_in_row_of_table('1: Learn Django')

        # He still sees a text box inviting him to add another item.
        # He enters "Use Django to build a web application"
        self.input_items_into_to_do_list('Use Django to build a web application')

        # The page updates again, and now shows both items on his list
        self.check_for_text_in_row_of_table('1: Learn Django')
        self.check_for_text_in_row_of_table('2: Use Django to build a web application')

        # Andrew wonders whether the site will remember his list.
        # Then, he sees that the site has generated a unique URL for him
        # -- because there is some explanatory text to that effect

        # He visits that URL, and his to-do list is still there.
        self.fail('SUCCESS!!, testing goat is pleased.\nBut Finish the test!')
        # Satisfied, he ends his short (but meaningful) existence

        browser.quit()
