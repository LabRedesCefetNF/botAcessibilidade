from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverFactory:
    def __init__(self):
        self.driver = None

    def create_driver(self):
        self.driver = webdriver.Firefox()
        # chrome_options = Options()
        # chrome_options.add_experimental_option("detach", True)
        # service = Service(ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver
