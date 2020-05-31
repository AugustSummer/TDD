from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

# Create your tests here.
'''class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1+1,3) '''
 
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found=resolve('/') #resolve 是 Django 内部使用的函数，用于解析 URL，并将其映射到相应的视图函数上。
        self.assertEqual(found.func,home_page) #检查解析网站根路径“/”时，是否能找到名为 home_page 的函数。
           
           
