from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_exist(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expect_html = render_to_string('home.html')
        #content 는 바이트 문자열임으로 decode를 통해 파이썬 유니코드문자열로 변환
        self.assertEqual(response.content.decode(), expect_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        item_text = "신규 작업 아이템"
        request.POST['item_text'] = item_text

        response = home_page(request)

        self.assertIn(item_text, response.content.decode())
        expect_html = render_to_string('home.html', {'new_item_text' : item_text })
        self.assertEqual(response.content.decode(), expect_html)

from lists.models import Item

class ItemModelTest(TestCase):

    def test_saveing_and_retrieving_items(self):
        first_item = Item()
        first_text = '첫 번째 아이템'
        first_item.text = first_text
        first_item.save()

        second_item_item = Item()
        second_text = '두 번째 아이템'
        second_item_item.text = second_text
        second_item_item.save()

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        first_saved_item = saved_item[0]
        second_saved_item = saved_item[1]

        self.assertEqual(first_saved_item.text, first_text)
        self.assertEqual(second_saved_item.text, second_text)


