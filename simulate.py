# -* - coding: UTF-8 -* -
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# driver = webdriver.PhantomJS()
# driver.get('http://tech.sina.com.cn/')
# # input = driver.find_elements(By.XPATH, u"//a[contains(text(),'下一页')]")
# # print input[0].click()
# # input = driver.find_elements(By.id, u"subShowContent1_loadMore")
# # print
#
# input = driver.find_elements(By.XPATH, u"//div[4]/div/h2/a")
#
# input = driver.find_elements(By.ID, u"subShowContent1_loadMore")
# input[0].click()
# inputs = driver.find_elements(By.XPATH, u"//div/div/h2/a")
# for input in inputs:
# 	print input.get_attribute(u'text')


driver = webdriver.PhantomJS()
driver.get('http://tech.sina.com.cn/internet/')

def scrollDown(driver, height):
	driver.execute_script("window.scrollBy(0,4500)", "")

foot = driver.find_element(By.XPATH, u"//a[contains(text(),'新浪科技意见反馈留言板')]")
print foot.size
print foot.location['y']
scrollDown(driver, 234)
time.sleep(1)
foot = driver.find_element(By.XPATH, u"//a[contains(text(),'新浪科技意见反馈留言板')]")
print foot.size
print foot.location['y']

input = driver.find_elements(By.ID, u"subShowContent1_loadMore")
input[0].click()
inputs = driver.find_elements(By.XPATH, u"//div/div/h2/a")
for input in inputs:
	print input.get_attribute(u'text')