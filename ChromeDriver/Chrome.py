from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
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
        from ctypes import windll
        from typing import Tuple

        self.window_width = windll.user32.GetSystemMetrics(0)
        self.window_height = windll.user32.GetSystemMetrics(1)
        self.width, self.height = 950, 700
        self.set_window_size(self.width, self.height)
        self.center: Tuple = (self.window_width // 2) - (self.width // 2), (self.window_height // 2) - (self.height // 2)
        self.set_window_position(self.center[0], self.center[1])

    def click_element(self, by: By, element: str, timeout: float = 10):
        WebDriverWait(self, timeout=timeout).until(ec.element_to_be_clickable((by, element)))
        self.find_element(by, element).click()

    def send_keys(self, by: By, element: str, value: str, timeout: float = 10):
        WebDriverWait(self, timeout=timeout).until(ec.visibility_of_element_located((by, element)))
        self.find_element(by, element).send_keys(value)

    def send_file(self, by: By, element: str, filename: str, timeout: float = 10):
        WebDriverWait(self, timeout=timeout).until(ec.visibility_of_all_elements_located((By.TAG_NAME, 'html')))
        self.find_element(by, element).send_keys(filename)

    def get_element(self, by: By, element: str, timeout: float = 10) -> WebElement:
        WebDriverWait(self, timeout=timeout).until(ec.visibility_of_element_located((by, element)))
        return self.find_element(by, element)
