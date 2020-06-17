import time

import pychrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def output_on_start(**kwargs):
    print "STARTED ", kwargs

def output_on_end(**kwargs):
    print "FINISHED ", kwargs

options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=8000")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

dev_tools = pychrome.Browser(url="http://localhost:8000")
tab = dev_tools.list_tab()[0]
tab.start()

start = time.time()
driver.get("https://fox.com")
print int(time.time() - start)

tab.call_method("Network.emulateNetworkConditions",
                offline=False,
                latency=100,
                downloadThroughput=9375,
                uploadThroughput=3125,
                connectionType="cellular3g")

tab.call_method("Network.enable", _timeout=20)
tab.set_listener("Network.requestWillBeSent", output_on_start)
tab.set_listener("Network.responseReceived", output_on_end)

start = time.time()
driver.get("https://fox.com")
print int(time.time() - start)
