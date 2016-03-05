from selenium import webdriver
from unittest import TestCase

class Functional_Test(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        #암묵적인 대기
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_enter_website(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do' , self.browser.title)



