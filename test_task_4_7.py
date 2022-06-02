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

def main_page(driver):
    driver.get("http://localhost/litecart")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"li.product")))
    if (are_elements_present(driver, By.CSS_SELECTOR, "li.product")):
        products = driver.find_elements(By.CSS_SELECTOR, "li.product")
        for product in products:
            assert len(product.find_elements(By.CSS_SELECTOR, "div.sticker")) == 1, "Stiker count <> 1"

def test_main_page(driverChrome):
    main_page(driverChrome)