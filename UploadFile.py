from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
picture = "E:\Development\Webdriver-Tutorials\pic.png"

# driver.get("https://www.filedropper.com/")
# driver.find_element(By.ID, "uploadFile").send_keys(picture)

# driver.get("http://s000.tinyupload.com/index.php")
# driver.find_element(By.NAME, "uploaded_file").send_keys(picture)
# driver.find_element(By.XPATH, "//img[@alt = 'Upload']").click()

# driver.get("http://png2jpg.com/")
# driver.find_element(By.XPATH, "//input[@type = 'file']").send_keys(picture)

driver.get("https://convertio.co/")
driver.find_element(By.XPATH, "//input[@type = 'file']").send_keys(picture)
