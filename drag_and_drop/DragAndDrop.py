import subprocess
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


# ============== JQuery Example ==============
driver = webdriver.Chrome()
driver.get("http://jqueryui.com/resources/demos/sortable/connect-lists.html")
draggable = driver.find_element(By.XPATH, "//ul[@id = 'sortable1']/li[1]")
droppable = driver.find_element(By.XPATH, "//ul[@id = 'sortable2']/li[1]")
# Option 1
ActionChains(driver).drag_and_drop(draggable, droppable).perform()

draggable2 = driver.find_element(By.XPATH, "//ul[@id = 'sortable1']/li[1]")
# Option 2
ActionChains(driver).click_and_hold(draggable2)\
                    .move_to_element(droppable)\
                    .release(draggable)\
                    .perform()


class HTML5:

    JQUERY_URL = "https://code.jquery.com/jquery-1.11.2.min.js"  # Change this url if you need a different version of jq
    JQUERY_LOAD_HELPER = "jquery_load_helper.js"
    DRAG_AND_DROP_HELPER = "drag_and_drop_helper.js"

    @staticmethod
    def __load_jquery(driver, jquery_url=JQUERY_URL):
        """
        :param driver: WebDriver object
        :param jquery_url: STRING, url from which to import jq
        :return: None
        """
        with open(HTML5.JQUERY_LOAD_HELPER) as f:
            load_jquery_js = f.read()
        # If JQ is already imported on the page, this wont overwrite it
        driver.execute_async_script(load_jquery_js, jquery_url)

    @staticmethod
    def drag_and_drop(driver, draggable, droppable):
        """
        :param driver: WebDriver object
        :param draggable: STRING, selector https://www.w3schools.com/jquery/jquery_selectors.asp
        :param droppable: STRING, selector https://www.w3schools.com/jquery/jquery_selectors.asp
        :return: None
        """
        HTML5.__load_jquery(driver)  # for the drag and drop js script to work, it needs to have jq

        with open(HTML5.DRAG_AND_DROP_HELPER) as f:  # getting js as a string from file and assigning to the variable
            drag_and_drop_js = f.read()

        drag_and_drop_command = "$('{draggable}').simulateDragDrop({{ dropTarget: '{droppable}'}});"\
                                .format(draggable=draggable, droppable=droppable)
        driver.execute_script(drag_and_drop_js + drag_and_drop_command)


# HTML 5 Example
driver = webdriver.Chrome()
driver.get("https://html5demos.com/drag/")
HTML5.drag_and_drop(driver, draggable="#one", droppable="#bin")

# HTML 4 Example - will not work
driver = webdriver.Chrome()
driver.get("http://gamehelp16.github.io/html4dragdrop/dragdrop.html")
HTML5.drag_and_drop(driver,
                    draggable="img:first",
                    droppable="input:first")


class Sikuli:

    __SIKULI = "C:\sikuli\\runsikulix.cmd"
    __DRAG_AND_DROP_HELPER = "E:\Development\Webdriver-Tutorials\drag_and_drop\drag_and_drop.sikuli"

    @staticmethod
    def drag_and_drop(draggable, droppable):
        """
        :param draggable: STRING, path to image that you want to drag
        :param droppable: STRING, path to image where you want to drop
        :return: None
        """
        process = subprocess.Popen("{sikuli} -r {script} --args \"{draggable}\" \"{dropabble}\""
                                   .format(sikuli=Sikuli.__SIKULI, script=Sikuli.__DRAG_AND_DROP_HELPER,
                                           draggable=draggable, dropabble=droppable),
                                   stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        process.wait()
        return output, error


# ============== Sikuli ==================
IMG_DIR = "E:\Development\Webdriver-Tutorials\drag_and_drop\drag_and_drop.sikuli"
# Web to Web
driver = webdriver.Chrome()
driver.get("http://gamehelp16.github.io/html4dragdrop/dragdrop.html")
Sikuli.drag_and_drop(draggable="{}\draggable.png".format(IMG_DIR),
                     droppable="{}\droppable.png".format(IMG_DIR))

# # Desktop to Web
driver = webdriver.Chrome()
driver.get("https://files.fm/")
Sikuli.drag_and_drop(draggable="{}\desktop.png".format(IMG_DIR),
                     droppable="{}\web.png".format(IMG_DIR))
