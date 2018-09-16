from selenium import webdriver


class Table:

    def __init__(self, driver):

        self.driver = driver

    def get_column_info(self):

        column_info = []
        columns = self.driver.find_elements_by_xpath("//header//span")
        for column in columns:
            column_info.append(str(column.text))
        return column_info

    def get_results(self, index=None):

        columns = self.get_column_info()
        data = {}
        elements = self.driver.find_elements_by_xpath("//div[@class = 'table-body']/div[contains(@class, 'table-row')]{}"
                                                      .format("[{}]".format(index) if index else ""))
        for element in elements:
            current_index = elements.index(element) + 1 if not index else index
            parsed_data = {}
            for column in columns:
                value = element.find_element_by_xpath("//div[contains(@class, 'table-row')][{}]"
                                                      "/div[contains(@class, 'table-row-column')][{}]"
                                                      .format(current_index, columns.index(column) + 1)).text
                parsed_data.update({column: str(value)})
            data.update({current_index: parsed_data})

        return data

    def get_number_of_results(self):

        return len(self.driver.find_elements_by_xpath("//div[@class = 'table-body']/div[contains(@class, 'table-row')]"))

    def click(self, column, value):

        if isinstance(column, str):
            column = self.get_column_info().index(column) + 1
        self.driver.find_element_by_xpath("//div[contains(@class, 'table-row-column')][{}]//*[text() = '{}']"
                                          .format(column, value)).click()

if "__main__" == __name__:

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.hackerrank.com/leaderboard")

    table = Table(driver)

    print table.get_column_info()
    print table.get_results()
    print table.get_results(index=2)
    print table.get_results(index=1)
    print table.get_number_of_results()
    table.click(column="Hacker", value="uwi")
