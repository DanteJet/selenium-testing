import time

import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driverChrome(request):
    # caps = DesiredCapabilities.CHROME
    # caps['goog:loggingPrefs'] = {'browser':'ALL' }
    # desired_capabilities = caps
    wd = webdriver.Chrome()
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def go_to_catalog(driver, wait):
    driver.get("http://localhost/litecart/admin/")
    wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="dataTable"]')))
    catalog_main = driver.find_element(By.CSS_SELECTOR, "ul.list-vertical li:nth-child(2)")
    catalog_main.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.list-vertical li:nth-child(2) li:nth-child(1)')))
    catalog = driver.find_element(By.CSS_SELECTOR, 'ul.list-vertical li:nth-child(2) li:nth-child(1)')
    catalog.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.dataTable tr:nth-child(3)')))
    rubber_ducks = driver.find_element(By.CSS_SELECTOR, 'table.dataTable tr:nth-child(3) a')
    rubber_ducks.click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/form/table/tbody/tr[9]')))

def check_products(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    button = driver.find_element(By.NAME, "login")
    button.click()
    wait = WebDriverWait(driver, 10)
    go_to_catalog(driver, wait)

    links_len = len(driver.find_elements(By.XPATH, '//*[@id="content"]/form/table/tbody/tr/td[3]/a'))
    links_len = links_len+4
    for link in range(5, links_len):
        duck = driver.find_element(By.XPATH,'//*[@id="content"]/form/table/tbody/tr['+str(link)+']/td[3]/a')
        duck.click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/h1')))
        #time.sleep(2)
        logs = driver.get_log('browser')
        assert len(logs)==0, "Logs bad("
        go_to_catalog(driver, wait)
    driver.close()

def test_admin_page(driverChrome):
    check_products(driverChrome)