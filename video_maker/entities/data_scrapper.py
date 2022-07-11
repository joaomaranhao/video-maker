from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options


class DataScrapper:
    def __init__(self) -> None:
        self.__download_path = r'C:\youtube\lol\replays'
        # SELENIUM
        self.__options = Options()
        self.__options.headless = True
        self.__options.set_preference(
            'browser.download.dir', self.__download_path)
        self.__options.set_preference("browser.download.folderList", 2)
        self.__options.add_argument('--log-level=3')
        self.driver = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()), options=self.__options)

    def quit(self):
        self.driver.quit()
