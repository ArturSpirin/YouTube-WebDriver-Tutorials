from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome("C:/webdrivers/chromedriver.exe")
driver = webdriver.Chrome(ChromeDriverManager().install())
