import subprocess
import time
import pywinauto  # Required, pip install -U pywinauto
import psutil  # Required, pip install psutil
from selenium import webdriver


class SystemDialog:

    RECURSION_LIMIT = 20

    def __init__(self, application_pid, dialog_title=None):

        self.__path_to_file = None
        self.__recursions = 0

        self.dialog_title = "Open" if dialog_title is None else dialog_title
        self.accept_button = "&SaveButton" if self.dialog_title == "Save As" else "&OpenButton"
        self.decline_button = "&CancelButton"

        app = pywinauto.application.Application()
        app.connect(process=application_pid)
        self.dialog = app.window(title=self.dialog_title)

    def __wait_for_dialog(self):
        start = time.time()
        while not self.dialog.exists() and (time.time() - start) <= 10:
            time.sleep(1)
        if not self.dialog.exists():
            raise Exception("System Dialog did not show in 10 seconds")

    def input_file_path(self, path_to_file):
        self.__wait_for_dialog()
        self.__path_to_file = path_to_file
        if path_to_file is not None:
            self.dialog.set_focus()
            self.dialog.Edit.type_keys(self.__path_to_file)
        return self

    def accept(self):
        if self.__recursions == SystemDialog.RECURSION_LIMIT:
            raise Exception("Not able to accept the System dialog.")

        self.__wait_for_dialog()
        self.dialog.set_focus()
        self.dialog[self.accept_button].click()

        if self.dialog.exists():
            self.__recursions += 1
            if self.__path_to_file is not None:
                return self.input_file_path(self.__path_to_file).accept()  # <--- FYI Recursion
            else:
                raise Exception("Trying to accept dialog without any inputs, not gonna work.")
        self.__recursions = 0

    def decline(self):
        if self.__recursions == SystemDialog.RECURSION_LIMIT:
            raise Exception("Not able to decline the System dialog.")

        self.__wait_for_dialog()
        self.dialog.set_focus()
        self.dialog[self.decline_button].click()

        if self.dialog.exists():
            self.__recursions += 1
            return self.decline()  # <--- Recursion
        self.__recursions = 0


driver = webdriver.Chrome()
driver.get("https://convertio.co/")
driver.find_element_by_xpath("(//label[@for='pc-upload-add'])[3]").click()

# process = psutil.Process(driver.service.process.pid)  # chromedriver pid
# pid = process.children()[0].pid  # chrome tab pid
#
# dialog = SystemDialog(application_pid=pid)
# dialog.input_file_path("E:\Development\Webdriver-Tutorials\system_dialogs\pic.png")
# dialog.accept()
# driver.quit()

SIKULI = "C:\sikuli\\runsikulix.cmd"
SCRIPT = "E:\Development\Webdriver-Tutorials\system_dialogs\system_dialogs.sikuli"

process = subprocess.Popen("{sikuli} -r {script} --args \"{accept}\" \"{file}\""
                           .format(sikuli=SIKULI, script=SCRIPT, accept=1,
                                   file="E:\Development\Webdriver-Tutorials\system_dialogs\pic.png"),
                           stdout=subprocess.PIPE, shell=True)
process.communicate()
process.wait()
# driver.quit()
