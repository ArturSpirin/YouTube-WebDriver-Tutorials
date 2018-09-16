import threading
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from BrowserManager import Browser


class UiObject:

    def __init__(self, by, locator):

        self.by = by
        self.locator = locator

    def get_element(self, wait=10):

        self.wait_to_appear(wait)
        return Browser.get_driver().find_element(self.by, self.locator)

    def get_all_elements(self, wait=10):

        self.wait_to_appear(wait)
        return Browser.get_driver().find_elements(self.by, self.locator)

    def get_locator(self):

        return self.locator

    def get_text(self, encoding=None):

        text = self.get_element().text
        return text.encode(encoding) if encoding else text

    def get_attribute(self, value):

        return self.get_element().get_attribute(value)

    def is_selected(self):

        return self.get_element().is_selected()

    def is_checked(self):

        return Browser.get_driver().execute_script("return arguments[0].checked;", self.get_element())

    def exists(self):

        try:
            WebDriverWait(Browser.get_driver(), 1).until(EC.presence_of_element_located((self.by, self.locator)))
            return True
        except:
            return False

    def is_clickable(self):

        def is_clickable(by, locator):
            try:
                WebDriverWait(Browser.get_driver(), 1).until(EC.element_to_be_clickable((by, locator)))
                return True
            except:
                return False

        return self.exists() and is_clickable(self.by, self.locator)

    def wait_to_be_clickable(self, seconds=10, ignore_error=False):

        start = time.time()
        while (time.time() - start) < seconds:
            if self.is_clickable():
                return self
            time.sleep(1)
        if not ignore_error:
            if self.exists():
                raise AssertionError("Locator in the DOM: {} but did not become click-able in {} seconds"
                                     .format(self.locator, seconds))
            raise AssertionError("Locator is not in the DOM and so not click-able: {}".format(self.locator))
        else:
            return self

    def wait_to_appear(self, seconds=10, ignore_error=False):

        start = time.time()
        while (time.time() - start) < seconds:
            if self.exists():
                return self
        if not ignore_error:
            raise AssertionError("Locator: {} did not appear in {} seconds!".format(self.locator, seconds))
        else:
            return self

    def wait_to_disappear(self, seconds=10, ignore_error=False):

        start = time.time()
        while (time.time() - start) < seconds:
            try:
                WebDriverWait(Browser.get_driver(), seconds).until(EC.invisibility_of_element_located((self.by, self.locator)))
            except Exception as error:
                if not ignore_error:
                    raise AssertionError("Locator: {} did not disappear in {} seconds! Error: {}"
                                         .format(self.locator, seconds, error.message))
        return self

    def click(self, wait=10, use_action_chains=False):

        self.wait_to_be_clickable(wait)
        initial_handles = Browser.get_driver().window_handles

        if use_action_chains:
            ui_object = self.get_element()
            ActionChains(Browser.get_driver()).move_to_element(ui_object).click().perform()
        else:
            try:
                self.get_element().click()
            except Exception as error:
                if "Other element would receive the click" in error.message:
                    self.scrollIntoCenter()
                    self.get_element().click()
                else:
                    raise error

        if len(Browser.get_driver().window_handles) > len(initial_handles):
            Browser.switch_to_latest_active_window()
        return self

    def set_text(self, value, loose_focus=False):

        self.get_element().clear()
        self.get_element().send_keys(str(value))
        if loose_focus:
            self.press_key(Keys.TAB)
        return self

    def scrollIntoCenter(self):

        scrollElementIntoMiddle = "var viewPortHeight = Math.max(document.documentElement.clientHeight, " \
                                  "window.innerHeight || 0); var elementTop = arguments[0].getBoundingClientRect().top;"\
                                  "window.scrollBy(0, elementTop-(viewPortHeight/2));"

        Browser.get_driver().execute_script(scrollElementIntoMiddle, self.get_element())

    def scrollIntoView(self):

        Browser.get_driver().execute_script("arguments[0].scrollIntoView()", self.get_element())
        return self

    def type_text(self, value):

        self.get_element().send_keys(value)
        return self

    def press_key(self, key, use_action_chains=False):

        if not use_action_chains:
            self.get_element().send_keys(key)
        else:
            chains = ActionChains(driver=Browser.get_driver())
            chains.send_keys(key).perform()
        return self

    def mouse_over(self):

        ui_object = self.get_element()
        ActionChains(Browser.get_driver()).move_to_element(ui_object).perform()
        return self


if "__main__" == __name__:

    buttons = ["Practice", "Compete", "Leaderboard"]

    def navigate(button):

        Browser.create_new_driver(Browser.CHROME)
        Browser.get_driver().get("https://www.hackerrank.com/dashboard")
        button_object = UiObject(By.XPATH, "//a[contains(@class, 'nav-link')]/span[text() = '{}']/parent::a".format(button))
        title = UiObject(By.XPATH, "//h1")
        button_object.click()
        time.sleep(2)
        print "Thread: {} URL: {} Title: {} Button Class: {}".format(threading.currentThread(),
                                                                     Browser.get_driver().current_url,
                                                                     title.get_text(),
                                                                     button_object.get_attribute("class"))
        Browser.shutdown()

    threads = []

    for button in buttons:
        thread = threading.Thread(target=navigate, args=(button,))
        thread.name = "[Thread: {}]".format(buttons.index(button))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
