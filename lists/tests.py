from django.test import TestCase
from django.urls import resolve  # resolve是Django用来解析URL的function，找到URL应该映射到哪个view
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item

# Create your tests here.
'''class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1+1,3) '''
 
class HomePageTest(TestCase):
    '''
    def test_root_url_resolves_to_home_page_view(self):
        found=resolve('/') #resolve 是 Django 内部使用的函数，用于解析 URL，并将其映射到相应的视图函数上。
        self.assertEqual(found.func,home_page) #检查解析网站根路径“/”时，是否能找到名为 home_page 的函数。
           
    def test_home_page_returns_correct_html(self):
        #request=HttpRequest()
        #response=home_page(request)
        response=self.client.get('/')
        html=response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-do lists</title>',html)
        self.assertTrue(html.endswith('</html>'))
        #excepted_html=render_to_string('home.html')
        #self.assertEqual(html,excepted_html)
        self.assertTemplateUsed(response,'home.html')'''
    
    # 重构后代码
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')
    
    
    def test_can_save_a_POST_request(self):
        self.client.post('/',data={'item_text':'A new list item'})
        
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')
        
        #self.assertIn('A new list item',response.content.decode())
        #self.assertTemplateUsed(response,'home.html')
        #self.assertEqual(response.status_code,302)
        #self.assertEqual(response['location'],'/')
        
    
    def test_redirects_after_POST(self):
        response=self.client.post('/',data={'item_text':'A new list item'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/')
        
    
    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)
    
    
    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        
        response=self.client.get('/')
        
        self.assertIn('itemey 1',response.content.decode())
        self.assertIn('itemey 2',response.content.decode())
        

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item =Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()
        
        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        
        first_item = saved_items[0]
        second_item = saved_items[1]
        #self.assertEqual(first_saved_item.text,'The first (ever) list item')
        #self.assertEqual(second_saved_item.text,'Item the second')
