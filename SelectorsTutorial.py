from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://google.com")

driver.find_element(By.ID, "lst-ib").send_keys("abc")

print "Button 1: ", driver.find_element(By.NAME, "btnK").get_attribute("value")
print "Button 2: ", driver.find_element(By.NAME, "btnI").get_attribute("value")
print "Img: ", driver.find_element(By.TAG_NAME, "img").get_attribute("src")
print "Label: ", driver.find_element(By.LINK_TEXT, "Gmail").text

# driver.find_element(By.NAME, "btnK").click()
driver.find_element(By.CLASS_NAME, "lsb").click()
driver.find_element(By.LINK_TEXT, "ABC Home Page - ABC.com").click()
# driver.find_element(By.PARTIAL_LINK_TEXT, "ABC Home Page").click()
