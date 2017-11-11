from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
browser.get("https://chromedino.com/")
body = browser.find_element_by_id('t')
while True:
	body.send_keys(Keys.ARROW_UP)