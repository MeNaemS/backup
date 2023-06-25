from checker.checker import Checker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


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


def yandex_backup(value: str, password: str):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = Chrome(options=options)
    driver.get('https://360.yandex.com/disk/')
    driver.click_element(By.ID, 'header-login-button')
    driver.send_keys(By.CSS_SELECTOR, 'input[type=text]', value)
    driver.click_element(By.ID, 'passp:sign-in')
    driver.send_keys(By.CSS_SELECTOR, 'input[type=password]', password)
    driver.click_element(By.ID, 'passp:sign-in')


if __name__ == '__main__':
    value = 'ilikesleeping268@ya.ru'
    check_adress = Checker(value)
    if check_adress.boolean is False:
        raise ValueError('Email address is not valid')
    password = 'GooglePasswordMadeWithMe100%'
    yandex_backup(value, password)
