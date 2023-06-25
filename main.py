from checker.checker import Checker
from ChromeDriver.Chrome import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


def yandex_backup(value: str, password: str):
    options = ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    driver = Chrome(options=options)
    driver.get('https://360.yandex.com/disk/')
    driver.click_element(By.ID, 'header-login-button')
    driver.send_keys(By.CSS_SELECTOR, 'input[type=text]', value)
    driver.click_element(By.ID, 'passp:sign-in')
    driver.send_keys(By.CSS_SELECTOR, 'input[type=password]', password)
    driver.click_element(By.ID, 'passp:sign-in')


if __name__ == '__main__':
    value = input()
    check_adress = Checker(value)
    if check_adress.boolean is False:
        raise ValueError('Email address is not valid')
    password = input()
    yandex_backup(value, password)
