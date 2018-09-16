from selenium import webdriver


class Dropdown:

    def __init__(self, driver, dropdown_id):

        self.driver = driver
        self.dropdown_id = dropdown_id
        self.dropdown = driver.find_element_by_id(dropdown_id)

    def select(self, value):

        self.dropdown.click()
        try:
            self.driver.find_element_by_xpath("//select[@id = '{}']/option[text() = '{}']"
                                              .format(self.dropdown_id, value)).click()
        except:
            print "Value: {} is not selectable in dropdown: {}".format(value, self.dropdown_id)
        return self

    def get_selected(self):

        return str(self.driver.find_element_by_xpath("//select[@id = '{}']/option[@selected]"
                                                     .format(self.dropdown_id)).text)

    def is_selected(self, value):

        return value == self.get_selected()

    def get_available_selections(self):

        data = []
        xpath = "//select[@id = '{}']/option".format(self.dropdown_id)
        count = len(self.driver.find_elements_by_xpath(xpath))
        for index in range(1, count + 1):
            data.append(str(self.driver.find_element_by_xpath("{}[{}]".format(xpath, index)).text))
        return data

if "__main__" == __name__:

    driver = webdriver.Chrome()
    driver.get("https://www.travelocity.com/#")

    rooms = Dropdown(driver, "package-rooms-hp-package")
    adults = Dropdown(driver, "package-1-adults-hp-package")
    children = Dropdown(driver, "package-1-children-hp-package")
    preferred_class = Dropdown(driver, "package-advanced-preferred-class-hp-package")

    dropdowns = [rooms, adults, children, preferred_class]
    for dropdown in dropdowns:
        print dropdown.get_selected()
        print dropdown.is_selected(1)
        print dropdown.get_available_selections()
        dropdown.select("2")
