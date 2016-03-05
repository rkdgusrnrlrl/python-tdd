from selenium import webdriver
from unittest import TestCase

from selenium.webdriver.common.keys import Keys


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

        head_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', head_text)

        #그녀는 바로 작업을 추가한다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업아이템입력')

        #공작깃털 사기라고 텍스트 박스에 입력한다
        inputbox.send_keys("공작깃털 사기")

        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1 : 공작깃털 사기' for row in rows),)




