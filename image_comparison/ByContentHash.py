import urllib.request
import hashlib
from selenium import webdriver


def hash_it(path):
    with open(path, 'rb') as f:
        hasher = hashlib.md5()
        hasher.update(f.read())
        return hasher.hexdigest()


directory = "E:/Development/Webdriver-Tutorials/image_comparison"
remote_img = "{}/{}".format(directory, "remote.png")
local_img = "{}/{}".format(directory, "local.png")

chrome = webdriver.Chrome()
chrome.get("https://github.com/ArturSpirin/test_junkie")
logo = chrome.find_element_by_xpath("//img[@alt='Test Junkie HTML Report Graphics']").get_attribute("src")

# urllib.urlretrieve(logo, remote_img)
urllib.request.urlretrieve(logo, remote_img)

local_img_hash = hash_it(local_img)
remote_img_hash = hash_it(remote_img)
assert local_img_hash == remote_img_hash, "Hashes do not match. {} vs {}".format(local_img_hash, remote_img_hash)
