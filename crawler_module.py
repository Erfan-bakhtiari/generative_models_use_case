import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    options = Options()
    # Add any options you need here
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def fetch_value(driver, url, selector):
    driver.get(url)
    element_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    ).text
    return element_value

def crawl(url, selectors, labels, result_container):
    driver = setup_driver()
    try:
        for selector, label in zip(selectors, labels):
            result_container[label] = fetch_value(driver, url, selector)
    finally:
        driver.quit()