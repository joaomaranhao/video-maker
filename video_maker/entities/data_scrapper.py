from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


class DataScrapper:
    def __init__(self) -> None:
        # SELENIUM
        self.__linux_binary_loation = '/usr/bin/brave-browser'
        self.__windows_binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
        self.__options = webdriver.ChromeOptions()
        self.__prefs = {'download.prompt_for_download': False,
                        'profile.default_content_settings.popups': 0,
                        }
        self.__options.add_experimental_option('prefs', self.__prefs)
        self.__options.headless = True
        # self.__options.binary_location = self.__linux_binary_loation
        self.__options.binary_location = self.__windows_binary_location
        self.driver = webdriver.Chrome(
            service=BraveService(
                ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
            options=self.__options)

    def quit(self):
        self.driver.quit()
