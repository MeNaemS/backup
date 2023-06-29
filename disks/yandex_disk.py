from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from ChromeDriver.Chrome import ChromeOptions, Chrome
from time import sleep


# Setting options for driver object, returns object: ChromeOptions.
# Used in the yandex_backup function.
def add_options() -> ChromeOptions:
    options = ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    return options


# Specifies from the user whether he wants to use the phone number, warning about possible errors, returns a tuple.
# Used in the yandex_backup function.
def rectification(value: str, option: str) -> (str, str):
    warning = [
        'Continued use of a phone number when logging into Yandex disk may result in an error sending a code to the number.',
        'Are you sure you want to use phone number login?',
        '1 — Yes.',
        '0 — No.'
    ]
    print('\n'.join(warning))
    while True:
        re_elect = input()
        if re_elect in ['0', '1']: break
        print('Incorrect response number')
    return (input('Please enter your email address from Yandex Disk: '), 'email') if re_elect == '0' else (value, option)


# Finding elements of type button[data-type="login"] and button[data-type="phone"] to determine the active button.
# Used in the log_in function.
def definition_of_active_button(driver: Chrome, option: str):
    option_button = [
        driver.find_element(By.CSS_SELECTOR, 'button[data-type="login"]'),
        driver.find_element(By.CSS_SELECTOR, 'button[data-type="phone"]')
    ]
    if (option == 'email') and (option_button[0].get_attribute('aria-pressed') == 'false'): option_button[0].click()
    elif (option == 'phone') and (option_button[1].get_attribute('aria-pressed') == 'false'): option_button[1].click()


# Gets the code input object, if any, and prints the results to the console, otherwise fails.
# Used in the log_in function
def phone_log(driver: Chrome, value: str, timeout: float = 1.5):
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.common.exceptions import TimeoutException

    driver.send_keys(By.ID, 'passp-field-phone', value)
    WebDriverWait(driver, timeout).until(ec.visibility_of_element_located((By.ID, 'passp-field-phoneCode')))
    while True:
        code = input('Enter activation code: ')
        if len(code) != 6:
            print('Wrong code size')
            continue
        driver.send_keys(By.ID, 'passp-field-phoneCode', code)
        error_code = driver.find_element(By.ID, 'passp-field-phoneCode')
        sleep(0.4)
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


# Clears the text field.
# Used in the input_attempt function.
def __clear__(driver: Chrome, element: WebElement):
    for _ in range(len(element.get_attribute('value'))):
        driver.send_keys(By.ID, element.get_attribute('id'), '\b')


# Attempting to enter data in a text field, if the site displays an error, then the user must change the password.
# Used in the email_log function.
def input_attempt(driver: Chrome, element: WebElement, value: str):
    while True:
        driver.send_keys(By.ID, element.get_attribute('id'), value)
        driver.click_element(By.ID, 'passp:sign-in')
        sleep(0.4)
        if element.get_attribute('aria-invalid') == 'true':
            print('There is no such account. Check your login or login by phone.' if element.get_attribute('name') == 'login' else 'Incorrect password.')
            __clear__(driver, element)
            value = input(f'Enter the modified {"email address" if element.get_attribute("name") == "login" else "password"}: ')
        else: break


# Logging into your account using email.
# Used in the log_in function.
def email_log(driver: Chrome, value: str, password: str):
    input_attempt(driver, driver.find_element(By.ID, 'passp-field-login'), value)
    input_attempt(driver, driver.find_element(By.ID, 'passp-field-passwd'), password)


# The function of logging into an account in Yandex Disk.
# Used in the yandex_backup function.
def log_in(driver: Chrome, value: str, password: str, option: str):
    driver.click_element(By.ID, 'header-login-button')
    definition_of_active_button(driver, option)
    email_log(driver, value, password) if option == 'email' else phone_log(driver, value)


# Actions with Yandex Account and Yandex Disk.
# Used in main.py file.
def yandex_backup(value: str, password: str, option: str, file_path: str):
    if option == 'phone': value, option = rectification(value, option)
    options = add_options()
    driver = Chrome(options=options)
    driver.get('https://360.yandex.com/disk/')
    log_in(driver, value, password, option)
    for file in file_path:
        driver.send_file(By.CSS_SELECTOR, 'input[type=file]', file)
