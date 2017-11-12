from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import time

browser = webdriver.Chrome()
browser.get("https://chromedino.com/")
body = browser.find_element_by_id('t')
while True:
	wait_time = np.random.uniform(0,1)
	body.send_keys(Keys.ARROW_UP)
	time.sleep(wait_time)