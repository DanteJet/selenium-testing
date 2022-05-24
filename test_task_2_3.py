import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.XPATH,'//*[@id="box-login"]/form/div[1]/table/tbody/tr[1]/td[2]/span/input')\
        .send_keys("admin")
    driver.find_element(By.XPATH, '//*[@id="box-login"]/form/div[1]/table/tbody/tr[2]/td[2]/span/input') \
        .send_keys("admin")
    button = driver.find_element(By.XPATH, '//*[@id="box-login"]/form/div[2]/button')
    button.click()
    time.sleep(5)
