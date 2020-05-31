from selenium import webdriver

browser = webdriver.Firefox()		# 启动一个 selenium webdriver，打开一个 Firefox 浏览器窗口
browser.get('http://localhost:8000')	# 打开本地电脑的网页

assert 'Django' in browser.title		# 做一个断言测试，检查这个网页的标题中是否含有单词‘Django’