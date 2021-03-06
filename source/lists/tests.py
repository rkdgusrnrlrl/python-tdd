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

from lists.models import Item, List


class ListAndItemModelTest(TestCase):

    def test_saveing_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_text = '첫 번째 아이템'
        first_item.text = first_text
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_text = '두 번째 아이템'
        second_item.text = second_text
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_);

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        first_saved_item = saved_item[0]
        second_saved_item = saved_item[1]

        self.assertEqual(first_saved_item.text, first_text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_text)
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
     def test_displays_only_items_for_that_list(self):
         list_ = List.objects.create()

         Item.objects.create(text="itemey 1", list=list_)
         Item.objects.create(text="itemey 2", list=list_)

         response = self.client.get('/lists/%d/' % (list_.id))

         self.assertContains(response, 'itemey 1')
         self.assertContains(response, 'itemey 2')

     def test_uses_list_template(self):
         list_ = List.objects.create()
         response = self.client.get('/lists/%d/' % (list_.id))
         self.assertTemplateUsed(response, 'list.html')

     def test_passes_correct_list_to_temlate(self):
         other_list = List.objects.create()
         currect_list = List.objects.create()
         response = self.client.post('/lists/%d/' % (currect_list.id))
         self.assertEqual(response.context['list'], currect_list)

class NewListTest(TestCase):
    def test_home_page_can_save_a_POST_request(self):
        item_text = '신규 작업 아이템'
        self.client.post('/lists/new', data={'item_text' : ('%s' % item_text)})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()

        self.assertEqual(new_item.text, item_text)

    def test_home_page_redirect_after_POST(self):
        item_text = '신규 작업 아이템'
        response = self.client.post('/lists/new', data={'item_text' : ('%s' % item_text)})
        list_ = List.objects.first()
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, '/lists/%d/' % (list_.id))

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        currect_list = List.objects.create()

        self.client.post('/lists/%d/add_item' % (currect_list.id)
                         , data={'item_text' : '기존 목록에 신규 아이템'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '기존 목록에 신규 아이템')
        self.assertEqual(new_item.list, currect_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        currect_list = List.objects.create()

        response = self.client.post('/lists/%d/add_item' % (currect_list.id)
                         , data={'item_text' : '기존 목록에 신규 아이템'})

        self.assertRedirects(response, 'lists/%d/' % (currect_list.id))




