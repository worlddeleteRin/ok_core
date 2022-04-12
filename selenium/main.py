from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import time

from ok_core.user.main import OkUser
import logging

logger = logging.getLogger(__name__)

def launch_default_selenium_driver() -> WebDriver:
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(
        options=chrome_options
    )
    return driver

def default_selenium_login(
    wd: WebDriver,
    user: OkUser
):
    logger.warning(f'user is {user.dict()}')
    # target elements
    email_input: WebElement = wd.find_element_by_id("field_email")
    password_input: WebElement = wd.find_element_by_id("field_password")
    login_button: WebElement = wd.find_element_by_class_name("button-pro.__wide")

    # clear inputs
    email_input.clear()
    password_input.clear()

    email_input.send_keys(user.username)
    password_input.send_keys(user.password)

    login_button.click()
