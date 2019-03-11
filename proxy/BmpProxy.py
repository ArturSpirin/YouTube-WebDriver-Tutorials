import pprint
import time

from browsermobproxy import Server
from selenium import webdriver


class ProxyManger:

    __BMP = "C:/Users/aspir/Downloads/browsermob-proxy-2.1.4-bin/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"

    def __init__(self):
        self.__server = Server(ProxyManger.__BMP)
        self.__client = None

    def start_server(self):
        self.__server.start()
        return self.__server

    def start_client(self):
        self.__client = self.__server.create_proxy(params={"trustAllServers": "true"})
        return self.__client

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server


if "__main__" == __name__:

    proxy = ProxyManger()
    server = proxy.start_server()
    client = proxy.start_client()
    client.new_har("google.com")
    print(client.proxy)

    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format(client.proxy))
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.google.com/")
    time.sleep(3)

    pprint.pprint(client.har)

    server.stop()
