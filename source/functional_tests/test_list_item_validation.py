from functional_tests.base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_connot_add_empty_list_items(self):
        # 메디스는 메인 페이지에 접속해서 빈 아이켐을 실수로 등록하려고 한다
        # 이렵 상자가 비어 있는 상태에서 엔터키를 누른다.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # 페이지는 새로고침 되고 빈아템을 등록할 수 없다는
        # 에러 메시지가 표시된다
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "빈 아이템을 등록 할 수 없습니다.")

        # 다른 아이템을 입력하고 이번에는 정상 처리된다
        self.browser.find_element_by_id('id_new_item').send_keys("우유사기\n")
        self.check_for_row_in_list_table('1: 우유사기')

        # 그녀는 고의적으로 다시 빈 아이템을 등록한다.
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # 리스트 페이지에 다시 에러 메시지가 표시된다.
        self.check_for_row_in_list_table('1: 우유사기')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "빈 아이템을 등록 할 수 없습니다.")

        # 아이템을 입력하면 정상 동작 한다.
        self.browser.find_element_by_id('id_new_item').send_keys("tea 만들기\n")
        self.check_for_row_in_list_table('1: 우유사기')
        self.check_for_row_in_list_table('2: tea 만들기')
