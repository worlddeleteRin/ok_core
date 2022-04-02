from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time

from selenium.webdriver.remote.webelement import WebElement
import time

start_execution_time = time.time()

def print_exec_time():
    e_time = time.time() - start_execution_time
    print("Execution time: ",e_time)

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
# chrome_options.add_argument("--window-size=1920,1080")
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

# driver.get("https://google.com/")
# driver.get("https://chakra-ui.com/")
driver.get("https://ok.ru/")

driver.get_screenshot_as_file("scr.png")

try:
    # target elements
    email_input: WebElement = driver.find_element_by_id("field_email")
    password_input: WebElement = driver.find_element_by_id("field_password")
    login_button: WebElement = driver.find_element_by_class_name("button-pro.__wide")

    # clear inputs
    email_input.clear()
    password_input.clear()

    email_input.send_keys("+79785599286")
    password_input.send_keys("Worldhack0Rin")
    login_button.click()

    # go to group page
    time.sleep(2)
    driver.get("https://ok.ru/group/61638264422477")
    time.sleep(1)

    "GROUP_HEADER:154619355092301:0"
    post_id = "154621104051533"
    like_data_attribute = f"GROUP_HEADER:{post_id}:0"
    # post_like_element: WebElement = driver.find_element_by_id("154619355092301")
    like_el: WebElement = driver.find_element(
        by=By.XPATH,
        value=f"//*[@data-like-reference-id='{like_data_attribute}']"
        # By.xpath("//*[@data-id='table1']")
    )
    print('like el is ', like_el)

    driver.get_screenshot_as_file("scr.png")

    like_el.click()

    print_exec_time()

except Exception as e:
    print('cause error', e)
    print_exec_time()
    driver.close()

driver.close()

