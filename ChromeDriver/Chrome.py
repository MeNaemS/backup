from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class ChromeOptions(webdriver.ChromeOptions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.add_experimental_option('useAutomationExtension', False)


class Chrome(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_window_size(950, 700)
        self.set_window_position(250, 50)

    def click_element(self, by: By, element: str, timeout: float = 10):
        WebDriverWait(self, timeout=timeout).until(ec.element_to_be_clickable((by, element)))
        self.find_element(by, element).click()

    def send_keys(self, by: By, element: str, value: str, timeout: int = 10):
        WebDriverWait(self, timeout=timeout).until(ec.visibility_of_element_located((by, element)))
        self.find_element(by, element).send_keys(value)
