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

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_home_page_redirect_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        item_text = "신규 작업 아이템"
        request.POST['item_text'] = item_text

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_Items(self):
        todo01 = '작업01'
        Item.objects.create(text=todo01)
        todo02 = '작업02'
        Item.objects.create(text=todo02)

        request = HttpRequest()
        response = home_page(request)

        self.assertIn(todo01, response.content.decode())
        self.assertIn(todo02, response.content.decode())


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


