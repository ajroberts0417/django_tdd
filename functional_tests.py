from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    # set up is always called at the beginning of the test
    def setUp(self):
        self.browser = webdriver.Firefox()

    # tearDown is always called at the end, even if the test fails
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Andrew was born to learn about a cool new online to-do app.
        # He goes to check out its homepage
        self.browser.get('http://localhost:8000')

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
        inputbox.send_keys('Learn Django')

        # When he hits ENTER, the page updates, and now it lists:
        # "1: Learn Django" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn('1: Learn Django', [row.text for row in rows]) #check for "1: Learn Django" in a list of all the rows of the table

        # He still sees a text box inviting him to add another item.
        # He enters "Use Django to build a web application"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use Django to build a web application')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on his list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Learn Django', [row.text for row in rows])
        self.assertin('2: Use Django to build a web application', [row.text for row in rows])

        # Andrew wonders whether the site will remember his list.
        # Then, he sees that the site has generated a unique URL for him
        # -- because there is some explanatory text to that effect

        # He visits that URL, and his to-do list is still there.
        self.fail('SUCCESS!!, testing goat is pleased.\nBut Finish the test!')
        # Satisfied, he ends his short (but meaningful) existence

        browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
