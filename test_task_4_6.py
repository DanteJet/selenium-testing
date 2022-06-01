import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driverChrome(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def are_elements_present(driver, *args):
    return len(driver.find_elements(*args)) > 0

def login_page(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    button = driver.find_element(By.NAME, "login")
    button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//li[@id="app-"]')))
    if(are_elements_present(driver, By.XPATH, '//li[@id="app-"]')):
        li_all = len(driver.find_elements(By.XPATH,'//li[@id="app-"]'))
        for i in range(1, li_all+1):
            lis = driver.find_element_by_css_selector("ul#box-apps-menu> li:nth-child(%d)"%i)
            lis.click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1")))
            len_sub = len(driver.find_elements(By.CSS_SELECTOR, "ul.docs > li"))
            for j in range(1, len_sub+1):
                l = driver.find_element_by_css_selector("ul.docs > li:nth-child(%d)"%j)
                l.click()
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1")))

def test_login_page(driverChrome):
    login_page(driverChrome)