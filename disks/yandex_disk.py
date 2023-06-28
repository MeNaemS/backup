from selenium.webdriver.common.by import By
from ChromeDriver.Chrome import ChromeOptions, Chrome
import time


# Setting options for driver object, returns object: ChromeOptions.
# Used in the yandex_backup function.
def add_options() -> ChromeOptions:
    options = ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    return options


# Finding elements of type button[data-type="login"] and button[data-type="phone"] to determine the active button.
# Used in the log_in function.
def definition_of_active_button(driver: Chrome, option: str):
    option_button = [
        driver.find_element(By.CSS_SELECTOR, 'button[data-type="login"]'),
        driver.find_element(By.CSS_SELECTOR, 'button[data-type="phone"]')
    ]
    active_email_button = (option == 'email') and (option_button[0].get_attribute('aria-pressed') == 'false')
    active_phone_button = (option == 'phone') and (option_button[1].get_attribute('aria-pressed') == 'false')
    if active_email_button:
        option_button[0].click()
    elif active_phone_button:
        option_button[1].click()


# The function of logging into an account in Yandex Disk.
# Used in the yandex_backup function.
def log_in(driver: Chrome, value: str, password: str, option: str):
    driver.click_element(By.ID, 'header-login-button')
    definition_of_active_button(driver, option)
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
    for _ in range(10):
        if driver.current_url != password_url: break
        time.sleep(0.5)
    if driver.current_url == password_url: raise ValueError("Incorrect password")


def yandex_backup(value: str, password: str, option: str, file_path: str):
    options = add_options()

    driver = Chrome(options=options)
    driver.get('https://360.yandex.com/disk/')
    log_in(driver, value, password, option)
    for file in file_path:
        driver.send_file(By.CSS_SELECTOR, 'input[type=file]', file)
      
