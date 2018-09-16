import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Browser:

    CHROME = 1
    FF = 2
    PHANTOM = 3
    IE = 4
    OPERA = 5

    __DRIVER_MAP = {}

    @staticmethod
    def create_new_driver(driver_id):

        thread_object = threading.currentThread()

        def get_driver():
            if Browser.PHANTOM == driver_id:
                driver = webdriver.PhantomJS()

            elif Browser.CHROME == driver_id:
                driver = webdriver.Chrome()

            elif Browser.FF == driver_id:
                driver = webdriver.Firefox()

            elif Browser.OPERA == driver_id:
                driver = webdriver.Opera()

            elif Browser.IE == driver_id:
                driver = webdriver.Ie()
            else:
                raise Exception("There is no support for driver_id: {}".format(driver_id))
            return driver

        Browser.__map(thread_object, get_driver())
        return Browser.get_driver()

    @staticmethod
    def get_driver():
        # print "Getting  driver for thread: {}".format(threading.currentThread())
        return Browser.__DRIVER_MAP[threading.current_thread()]["driver"]

    @staticmethod
    def shutdown():

        Browser.get_driver().quit()

    @staticmethod
    def __map(thread, driver):

        Browser.__DRIVER_MAP[thread] = {"driver": driver}

    @staticmethod
    def get_driver_map():
        return Browser.__DRIVER_MAP

    @staticmethod
    def back():

        Browser.get_driver().back()

    @staticmethod
    def forward():

        Browser.get_driver().forward()

    @staticmethod
    def open_new_tab():
        Browser.get_driver().find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

    @staticmethod
    def switch_to_window(window):
        Browser.get_driver().switch_to_window(window)

    @staticmethod
    def switch_to_latest_active_window():
        windows = Browser.get_driver().window_handles
        if len(windows) == 1:
            Browser.get_driver().switch_to_window(windows[0])
            return
        for index in range(1, len(windows)):
            Browser.get_driver().switch_to_window(windows[-index])
            return

    @staticmethod
    def close_current_active_window():
        windows = Browser.get_driver().window_handles
        if len(windows) == 1:
            return
        for index in range(1, len(windows)):
            Browser.get_driver().close()
            Browser.switch_to_latest_active_window()
            return


if "__main__" == __name__:

    urls = ["https://www.hackerrank.com/dashboard",
            "https://www.hackerrank.com/contests",
            "https://www.hackerrank.com/jobs/search",
            "https://www.hackerrank.com/leaderboard"]

    threads = []

    def get_url(_url):
        Browser.create_new_driver(Browser.CHROME)
        Browser.get_driver().get(_url)
        print "Thread: {} URL: {}".format(threading.currentThread(), Browser.get_driver().current_url)
        Browser.shutdown()

    for url in urls:
        thread = threading.Thread(target=get_url, args=(url,))
        thread.name = "[Thread: {}]".format(urls.index(url))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
