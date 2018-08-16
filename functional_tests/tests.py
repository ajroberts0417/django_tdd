from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 5

## make our test, inheriting from LiveServerTestCase (a django testing class)
class NewVisitorTest(StaticLiveServerTestCase):

    ## set up is always called at the beginning of the test
    def setUp(self):
        ## browser is an object owned by the NewVisitorTest class
        self.browser = webdriver.Firefox()

    ## tearDown is always called at the end, even if the test fails
    def tearDown(self):
        self.browser.quit()

    ## Helper function: checks if row_text is in any of the rows of the list
    ## But does so while waiting smartly so as not to throw an exception
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.2)

    ## Helper function: adds any number of items to the to-do list
    ## via the inputbox in the website, and returns the inputbox
    def input_items_into_to_do_list(self, *input_items):
        inputbox = self.browser.find_element_by_id('id_new_item')
        for item in input_items:
            inputbox.send_keys(item)
            inputbox.send_keys(Keys.ENTER)
        return inputbox

    def test_layout_and_styling(self):
        # Andrew goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )

        # He starts a new list and the input is nicely centered, too
        self.input_items_into_to_do_list('testing')
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )


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
        self.wait_for_row_in_list_table('1: Learn Django')

        # He still sees a text box inviting him to add another item.
        # He enters "Use Django to build a web application"
        self.input_items_into_to_do_list('Use Django to build a web application')

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('1: Learn Django')
        self.wait_for_row_in_list_table('2: Use Django to build a web application')

        # Andrew wonders whether the site will remember his list.
        # Then, he sees that the site has generated a unique URL for him
        # -- because there is some explanatory text to that effect

        # He visits that URL, and his to-do list is still there.
        self.fail('SUCCESS!!, testing goat is pleased.\nBut Finish the test!')
        # Satisfied, he ends his short (but meaningful) existence

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Andrew starts a new to-do list
        self.browser.get(self.live_server_url)
        self.input_items_into_to_do_list('Learn Django')
        self.wait_for_row_in_list_table('1: Learn Django')

        #Andrew notices that his list has a unique URL
        andrew_list_url = self.browser.current_url
        self.assertRegex(andrew_list_url, '/lists/.+')

        #Now, a new user, Ivette, is born and comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Andrew's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Ivette visits the home page. There is no sign of Andrew's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Learn Django', page_text)
        self.assertNotIn('Use Django', page_text)

        # Ivette starts her own new list
        self.input_items_into_to_do_list('Buy a bassoon')
        self.wait_for_row_in_list_table('1: Buy a bassoon')

        # Ivette gets her own unique url
        ivette_list_url = self.browser.current_url
        self.assertRegex(ivette_list_url, 'lists/.+')
        self.assertNotEqual(ivette_list_url, andrew_list_url)

        # Again, there is no trace of Andrew's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Learn Django', page_text)

        # Her list is there, however.
        self.assertIn('Buy a bassoon', page_text)

        # Satisfied, they both end their short but meaningful existence
