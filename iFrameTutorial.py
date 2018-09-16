from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://nunzioweb.com/iframes-example.htm")

iframes = driver.find_elements_by_tag_name("iframe")

driver.switch_to.frame(iframes[0])
print driver.find_element_by_id("mep_0").get_attribute("class")
driver.switch_to.default_content()

driver.switch_to.frame(iframes[1])
print driver.find_element_by_tag_name("img").get_attribute("src")
driver.switch_to.default_content()

driver.switch_to.frame(iframes[2])
print driver.find_element_by_link_text("Slick City").click()
driver.switch_to.default_content()
