
from selenium import webdriver
from functional_tests.base import FunctionalTest


class NewVistorTest(FunctionalTest):

    def test_enter_website(self):
        self.browser.get(self.server_url)
        self.assertIn('To-Do' , self.browser.title)

        #head_text = self.browser.find_element_by_tag_name('h1').text
        #self.assertIn('To-Do', head_text)

        #그녀는 바로 작업을 추가한다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업아이템입력')

        #공작깃털 사기라고 텍스트 박스에 입력한다

        todo01 = "공작깃털 사기"
        self.add_todo(inputbox, todo01)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')
        todo01_result = '1 : 공작깃털 사기'
        self.check_for_row_in_list_table(todo01_result)

        # 2번째 할일 등록 작업
        inputbox = self.browser.find_element_by_id('id_new_item')
        todo02 = '공작깃털을 이용해서 그물 만들기'
        self.add_todo(inputbox, todo02)

        todo02_result = '2 : 공작깃털을 이용해서 그물 만들기'
        self.check_for_row_in_list_table(todo01_result)
        self.check_for_row_in_list_table(todo02_result)

        #새로운 사용자인 프란시스가 사이트에 접속한다.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #프란시스가 홈페이지에 접속한다.
        #에디스의 리스트는 보이지 않는다.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(todo01, page_text)
        self.assertNotIn(todo02, page_text)

        #프란시스가 새로운 작업 아이템을 입력하기 시작한다.
        #그는 에디스보다 재미가 없다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        todo = '우유 사기'
        self.add_todo(inputbox, todo)

        #프란시스가 전용 URL 을 취득한다.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #에디스가 입력한 흔적없다는 것을 다시 확인한다.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(todo01, page_text)
        self.assertNotIn(todo02, page_text)


