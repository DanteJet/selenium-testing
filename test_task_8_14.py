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

def add_country(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    button = driver.find_element(By.NAME, "login")
    button.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//table[@class="dataTable"]')))
    catalog = driver.find_element(By.CSS_SELECTOR, "ul.list-vertical li:nth-child(3)")
    catalog.click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//td[@id="content"]/h1')))
    new_country = driver.find_element(By.XPATH, '//td[@id="content"]//a[@class="button"]')
    new_country.click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//td[@id="content"]/h1')))
    links = driver.find_elements(By.XPATH, '//*[@id="content"]//i[@class="fa fa-external-link"]')
    for link in links:
        currient_window = driver.current_window_handle
        link.click()
        wait.until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != currient_window:
                driver.switch_to.window(window_handle)
                break
        wait.until(EC.presence_of_element_located((By.XPATH, '//h1')))
        driver.close()
        driver.switch_to.window(currient_window)
        wait.until(EC.presence_of_element_located((By.XPATH, '//td[@id="content"]/h1')))

def test_admin_page(driverChrome):
    add_country(driverChrome)