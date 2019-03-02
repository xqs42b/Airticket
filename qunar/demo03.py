# coding=utf-8


import time
from selenium import webdriver


driver = webdriver.Chrome()
url = 'https://flight.qunar.com/'
driver.get(url)
time.sleep(1000)
