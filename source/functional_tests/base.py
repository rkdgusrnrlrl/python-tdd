import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


from selenium.webdriver.common.keys import Keys


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    def setUp(self):
        self.browser = webdriver.Firefox()
        #암묵적인 대기
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, todo01_result):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(todo01_result, [row.text for row in rows])

    def add_todo(self, inputbox, todo01):
        inputbox.send_keys(todo01)
        inputbox.send_keys(Keys.ENTER)

