import time
from checker.checker import Checker
from ChromeDriver.Chrome import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


def choose_file() -> str:
    import sys
    from PyQt5.QtWidgets import QFileDialog, QApplication

    app = QApplication(sys.argv)
    return QFileDialog.getOpenFileNames(caption='Choose files')[0]


def yandex_backup(value: str, password: str, option: str):
    options = ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    driver = Chrome(options=options)
    driver.get('https://360.yandex.com/disk/')
    driver.click_element(By.ID, 'header-login-button')
    option_button = [
        driver.find_element(By.CSS_SELECTOR, 'button[data-type="login"]'),
        driver.find_element(By.CSS_SELECTOR, 'button[data-type="phone"]')
    ]
    if (option == 'email') and (option_button[0].get_attribute('aria-pressed') == 'false'):
        option_button[0].click()
    if (option == 'phone') and (option_button[1].get_attribute('aria-pressed') == 'false'):
        option_button[1].click()
    time.sleep(0.5)
    driver.send_keys(By.CSS_SELECTOR, 'input[type=text]', value)
    driver.click_element(By.ID, 'passp:sign-in')
    time.sleep(0.5)
    login_url = 'https://passport.yandex.com/auth?retpath=https%3A%2F%2Fdisk.yandex.com'
    if driver.current_url == login_url:
        raise ValueError("Account doesn't exist")
    driver.send_keys(By.CSS_SELECTOR, 'input[type=password]', password)
    driver.click_element(By.ID, 'passp:sign-in')
    time.sleep(1)
    password_url = 'https://passport.yandex.com/auth/welcome?retpath=https%3A%2F%2Fdisk.yandex.com'
    if driver.current_url == password_url:
        raise ValueError("Incorrect password")


if __name__ == '__main__':
    file_path = choose_file()
    print(file_path)
    value = 'ilikesleeping268@ya.ru'
    check_adress = Checker(value)
    if check_adress.boolean is False:
        raise ValueError('Email address is not valid')
    if check_adress.option == 'phone':
        from sys import exit

        print('We apologize, at the moment support for a phone number for backup in Yandex Disk is not available')
        exit()
    password = 'GooglePasswordMadeWithMe'
    yandex_backup(value, password, check_adress.option)

