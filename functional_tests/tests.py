from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


'''第一章
browser = webdriver.Firefox()		# 启动一个 selenium webdriver，打开一个 Firefox 浏览器窗口
browser.get('http://localhost:8000')	# 打开本地电脑的网页

assert 'To-Do' in browser.title		# 1.做一个断言测试，检查这个网页的标题中是否含有单词‘Django’

browser.quit()'''

class NewVisitorTest(LiveServerTestCase):

	def setUp(self): # 测试之前运行，打开浏览器
		self.browser = webdriver.Firefox()
		# self.browser.implicitly_wait(3)

	def tearDown(self): # 测试之后运行，关闭浏览器
		self.browser.quit()
		
	def check_for_row_in_list_table(self,row_text):
		table=self.browser.find_element_by_id('id_list_table')
		rows=table.find_elements_by_tag_name('tr')
		self.assertIn(row_text,[row.text for row in rows])
	

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.live_server_url)
		# 网页的标题和头部都包含“To-Do”
		self.assertIn('To-Do', self.browser.title)
		header_text=self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do',header_text)
        # 输入回车后，页面更新
		# inputbox.send_keys(Keys.ENTER)
		# self.check_for_row_in_list_table('1:Buy peacock feathers')
		inputbox=self.browser.find_element_by_id('id_new_item')
        # 输入待办事项
		'''self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a To-do item'
		)'''
		inputbox.send_keys('Use peacock feathers to make a fly') #('Buy peacock feathers')
		#页面更新
		inputbox.send_keys(Keys.ENTER) # send_keys，Selenium在输入框中输入内容的方法
		time.sleep(1)
		
		# 页面再次更新，显示两个待办事项
		self.check_for_row_in_list_table('1:Buy peacock feathers')
		self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
		
		table=self.browser.find_element_by_id('id_list_table')
		rows=table.find_elements_by_tag_name('tr')
		self.assertIn('1:Buy peacock feathers',[row.text for row in rows])
		'''self.assertTrue(
			any(row.text=='1:Buy peacock feathers' for row in rows),
			#"New to-do item did not appear in table"
            f"New to-do item did not appear in table.Content were:\n{table.text}"
		)# f-string可以使用花括号添加变量'''
		self.assertIn(
			'2:Use peacock feathers to make a fly',
			[row.text for row in rows]
		)
		self.fail('Finish the test!')
		# Selenium 中 find_element_by... 和 find_elements_by... 这两类函数的区别。
		# 前者返回一个元素，如果找不到就抛出异常；后者返回一个列表，这个列表可能为空。

