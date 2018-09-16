from selenium import webdriver


class RadioButton:

    def __init__(self, driver, text):

        self.driver = driver
        self.text = text
        self.button = self.driver.find_element_by_xpath("//button[contains(@class, 'btn btnLrg btnSecondary') "
                                                        "and text() = '{}']".format(text))
    def is_selected(self):

        return "btnSelected" in self.button.get_attribute("class")

    def select(self):

        self.button.click()
        return self


class RadioButtonGroup:

    def __init__(self, radio_buttons):

        self.radio_buttons = radio_buttons

    def get_selected(self):

        for radio_button in self.radio_buttons:
            if radio_button.is_selected():
                return radio_button.text


if "__main__" == __name__:

    driver = webdriver.Chrome()
    driver.get("https://www.trulia.com/")

    buy = RadioButton(driver, "Buy")
    rent = RadioButton(driver, "Rent")
    sold = RadioButton(driver, "Sold")

    group = RadioButtonGroup([buy, rent, sold])
    print group.get_selected()

    buy.select()
    print group.get_selected()

    rent.select()
    print group.get_selected()

    sold.select()
    print group.get_selected()
