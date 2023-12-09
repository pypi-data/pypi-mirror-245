from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import asyncio

def open_website(url: str, headless: bool = True) -> WebDriver:
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu") 

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    return driver

async def scroll_to_bottom(driver: WebDriver) -> WebDriver:
    last_height = -1
    current_height = 0
    driver.switch_to.default_content()
    while last_height != current_height:
        last_height = current_height
        current_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script(f"window.scrollTo({current_height}, document.body.scrollHeight);")
        await asyncio.sleep(3)

async def accept_cookies_sport_nu(driver: WebDriver):
    await asyncio.sleep(5)
    iframe = driver.find_element("xpath", '//iframe[contains(@id, "sp_message_iframe_")]')
    driver.switch_to.frame(iframe)
    button = driver.find_element(By.CLASS_NAME, "sp_choice_type_11")
    button.click()

def doubleSplit(tag, first, last):
    try:
        return tag.decode().split(first)[1].split(last)[0]
    except:
        return tag.decode()