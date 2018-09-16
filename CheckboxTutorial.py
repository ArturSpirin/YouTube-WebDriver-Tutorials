from selenium import webdriver


class Checkbox:

    def __init__(self, driver, checkbox_id):

        self.checkbox_id = checkbox_id
        self.driver = driver
        self.checkbox = driver.find_element_by_id(checkbox_id)

    def is_enabled(self, use_js=True):

        if use_js:
            return self.driver.execute_script("return document.getElementById('{}').checked".format(self.checkbox_id))
        return "on" in self.checkbox.get_attribute("value")

    def enabled(self, enable):

        if (enable and not self.is_enabled()) or (not enable and self.is_enabled()):
            self.checkbox.click()
        else:
            print "Checkbox is already set to: {}".format(enable)
        return self

if "__main__" == __name__:

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.trulia.com/for_rent/Milpitas,CA")

    driver.find_element_by_id("moreToggle").click()

    appartment = Checkbox(driver, "homeType0")
    room = Checkbox(driver, "homeType1")
    single = Checkbox(driver, "homeType2")
    townhome = Checkbox(driver, "homeType3")

    checkboxes = [appartment, room, single, townhome]

    for checkbox in checkboxes:

        print checkbox.is_enabled()
        checkbox.enabled(True)
        checkbox.enabled(True)
        print checkbox.is_enabled()
