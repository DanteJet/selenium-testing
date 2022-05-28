import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driverFirefoxN(request):
    wd = webdriver.Firefox(firefox_binary="/Applications/FirefoxNightly.app/Contents/MacOS/firefox-bin")
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def login_page(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    button = driver.find_element(By.NAME, "login")
    button.click()
    time.sleep(5)

def test_login_page(driverFirefoxN):
    login_page(driverFirefoxN)