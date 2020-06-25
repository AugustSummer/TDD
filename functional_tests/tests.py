#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException
import os

'''第一章
browser = webdriver.Firefox()		# 启动一个 selenium webdriver，打开一个 Firefox 浏览器窗口
browser.get('http://localhost:8000')	# 打开本地电脑的网页

assert 'To-Do' in browser.title		# 1.做一个断言测试，检查这个网页的标题中是否含有单词‘Django’

browser.quit()'''

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

	def setUp(self): #测试之前运行，打开浏览器
		self.browser = webdriver.Firefox()
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server
		#self.live_server_url = 'http://101.37.168.209/'

	def tearDown(self): #测试之后运行，关闭浏览器
		#self.browser.refresh()
		self.browser.quit()
		
	'''def check_for_row_in_list_table(self,row_text):
		table=self.browser.find_element_by_id('id_list_table')
		rows=table.find_elements_by_tag_name('tr')
		self.assertIn(row_text,[row.text for row in rows])'''
	
	# 隐含方式的等待
	def wait_for_row_in_list_table(self,row_text):
		start_time = time.time()
		while True:
			try:
				table=self.browser.find_element_by_id('id_list_table')
				rows=table.find_elements_by_tag_name('tr')
				self.assertIn(row_text,[row.text for row in rows])
				return
			except (AssertionError,WebDriverException) as e:
				if time.time()-start_time > MAX_WAIT:
					return e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
		# Edith has heard about a cool new online to-do app. She goes to check out its page
		self.browser.get(self.live_server_url)
		
		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		# She is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		
		# She types "Buy peacock feathers" into a text box (Edith's hobby
		# is tying fly-fishing lures)
		inputbox.send_keys('Buy peacock feathers')
		
		# When she hits enter, the page updates, and now the page lists
		# "1: Buy peacock feathers" as an item in a to-do list table
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		
		# There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly" (Edith is very
		# methodical)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		
		# The page updates again,and now shows both items on her list 
		self.wait_for_row_in_list_table('1:Buy peacock feathers')
		self.wait_for_row_in_list_table('2:Use peacock feathers to make a fly')
		
		
		#Satisfied,she goes back to sleep
	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Edith starts a  new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1:Buy peacock feathers')
		
		# She notices that her list has a unique URL 
		edith_list_url = self.browser.current_url
		#self.assertRegex(edith_list_url,'/lists/.+')
		
		# We use a new browser session to make sure that no information
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		# Fracis visits the homepage.There is no sign of Edith's list 
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers',page_text)
		self.assertNotIn('mak a fly',page_text)
		
		# Fracis starts a new lis by entering a new item
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1:Buy milk')
		
		#Fracis gets his own unique URL
		francis_list_url = self.browser.current_url
		#self.assertRegex(francis_list_url,'/lists/.+')
		#self.assertNotEqual(francis_list_url,edith_list_url)
		
		# Again,there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers',page_text)
		self.assertIn('Buy milk',page_text)
		
		
	def test_layout_and_styling(self):
		#Edith goes to the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024,768)
		
		#She notices the inputbox is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x']+inputbox.size['width']/2,
			512,
			delta=10
			)
		
		# She starts a new list and sees the input is nicely
		# centered there too
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)
		
'''
	def test_can_start_a_list_and_retrieve_it_later(self):
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
		self.browser.get(self.live_server_url)
		
		#网页的标题和头部都包含“To-Do” 
		# She notice the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text=self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do',header_text)
		
		# 输入回车后，页面更新
		# inputbox.send_keys(Keys.ENTER)
		# self.check_for_row_in_list_table('1:Buy peacock feathers')
		
		#She is invited to enter a to-do item straight away
		inputbox=self.browser.find_element_by_id('id_new_item')
		# 输入待办事项
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		
		#She types “Buy peacock feathers” into a text box
		inputbox.send_keys('Buy peacock feathers') #('Use peacock feathers to make a fly') 
		
		#页面更新 
		#When she hits enter,the page updates,and now the page lists
		inputbox.send_keys(Keys.ENTER) # send_keys，Selenium在输入框中输入内容的方法
		#time.sleep(1)#明确等待
		#self.check_for_row_in_list_table('1:Buy peacock feathers')
		self.wait_for_row_in_list_table('1:Buy peacock feathers') 
		
		#There is still a text box inviting her to add another item
		inputbox=self.browser.find_element_by('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		#time.sleep(1)
		
		# 页面再次更新，显示两个待办事项
		# The page updates again,and now shows both items on her list
		self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
		self.check_for_row_in_list_table('1:Buy peacock feathers')
		
		#The page updates again,and now shows both items on her list
		#table=self.browser.find_element_by_id('id_list_table')
		#rows=table.find_elements_by_tag_name('tr')
		#self.assertIn('1:Buy peacock feathers',[row.text for row in rows])
		#self.assertTrue(
		#	any(row.text=='1:Buy peacock feathers' for row in rows),
		#	#"New to-do item did not appear in table"
		#	f"New to-do item did not appear in table.Content were:\n{table.text}"
		#)# f-string可以使用花括号添加变量
		#self.assertIn(
		#	'2:Use peacock feathers to make a fly',
		#	[row.text for row in rows]
		#)
        # Edith wonder whether the site whether the site will remember her list
		self.fail('Finish the test!')
        
        # She visits that URL - her to-do list is still there
        
        #Satisfied,she goes back to sleep
        
		# Selenium 中 find_element_by... 和 find_elements_by... 这两类函数的区别。
		# 前者返回一个元素，如果找不到就抛出异常；后者返回一个列表，这个列表可能为空。
'''

