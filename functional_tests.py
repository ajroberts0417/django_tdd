from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Andrew was born to learn about a cool new online to-do app.
        # He goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # He is invited to enter a to-do item straight away

        # He types "Learn Django" into a text box (because he is a software developer)

        # When he hits ENTER, the page updates, and now it lists:
        # "1: Learn Django" as an item in a to-do list

        # He still sees a text box inviting him to add another item.
        # He enters "Use Django to build a web application"

        # The page updates again, and now shows both items on his list

        # Andrew wonders whether the site will remember his list.
        # Then, he sees that the site has generated a unique URL for him
        # -- because there is some explanatory text to that effect

        # He visits that URL, and his to-do list is still there.

        # Satisfied, he ends his short (but meaningful) existence

        browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
