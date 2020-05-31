from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        [...]
    
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)