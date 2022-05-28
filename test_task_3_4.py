import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driverChrome(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

@pytest.fixture
def driverSafari(request):
    wd = webdriver.Safari()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

@pytest.fixture
def driverFirefox(request):
    wd = webdriver.Firefox()
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

def test_login_page(driverChrome, driverSafari, driverFirefox):
    login_page(driverChrome)
    login_page(driverFirefox)
    login_page(driverSafari)