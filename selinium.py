import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver_path = '/usr/local/bin/chromedriver'
brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'

option = webdriver.ChromeOptions()
option.binary_location = brave_path
driver = webdriver.Chrome(executable_path=driver_path, options=option)
driver.get('https://www.shudder.com/movies')

ScrollNumber = 50
for i in range(1,ScrollNumber):
    driver.execute_script('window.scrollTo(1,50000)')
    time.sleep(5)

file = open('DS.html', 'w')
file.write(driver.page_source)
file.close()

driver.close()