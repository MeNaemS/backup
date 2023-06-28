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
    if active_email_button: option_button[0].click()
    elif active_phone_button: option_button[1].click()


# Gets the code input object, if any, and prints the results to the console, otherwise fails.
# Used in the log_in function
def code_activation(driver: Chrome, timeout: float = 3):
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.common.exceptions import TimeoutException

    try:
        WebDriverWait(driver, timeout).until(ec.visibility_of_element_located((By.ID, 'passp-field-phoneCode')))
        while True:
            code = input('Enter activation code: ')
            if len(code) != 6:
                print('Wrong code size')
                continue
            driver.send_keys(By.ID, 'passp-field-phoneCode', code)
            error_code = driver.find_element(By.ID, 'passp-field-phoneCode')
            time.sleep(0.4)
            if error_code.get_attribute('aria-invalid') == 'true':
                print('Incorrect code')
                continue
            try:
                WebDriverWait(driver, timeout).until(ec.visibility_of_element_located(
                    (By.XPATH, '//*[@id="UserEntryFlow"]/form/div/div[3]/div/button'))
                )
                driver.click_element(By.XPATH, '//*[@id="UserEntryFlow"]/form/div/div[3]/div/button')
                driver.click_element(By.XPATH, '//*[@id="UserEntryFlow"]/form/div/div[3]/div/div/ul/li[2]/a')
                break
            except TimeoutException: break
        firstname = input('Enter your first name: ')
        driver.send_keys(By.ID, 'passp-field-firstname', firstname)
        lastname = input('Enter your last name: ')
        driver.send_keys(By.ID, 'passp-field-lastname', lastname)
        driver.click_element(By.CSS_SELECTOR, 'button[type=submit]')
        driver.click_element(By.CLASS_NAME, 'AccountsListItem-account')
    except TimeoutException: return None


# The function of logging into an account in Yandex Disk.
# Used in the yandex_backup function.
def log_in(driver: Chrome, value: str, password: str, option: str):
    driver.click_element(By.ID, 'header-login-button')
    definition_of_active_button(driver, option)
    driver.send_keys(By.ID, 'passp-field-login', value) if option == 'email' else driver.send_keys(By.ID, 'passp-field-phone', value)
    driver.click_element(By.ID, 'passp:sign-in')
    time.sleep(0.5)
    code_activation(driver)
    if option == 'email':
        driver.send_keys(By.CSS_SELECTOR, 'input[type=password]', password)
        driver.click_element(By.ID, 'passp:sign-in')
        time.sleep(1)


# Actions with Yandex Account and Yandex Disk.
# Used in main.py file.
def yandex_backup(value: str, password: str, option: str, file_path: str):
    options = add_options()
    driver = Chrome(options=options)
    driver.get('https://360.yandex.com/disk/')
    log_in(driver, value, password, option)
    for file in file_path:
        driver.send_file(By.CSS_SELECTOR, 'input[type=file]', file)
