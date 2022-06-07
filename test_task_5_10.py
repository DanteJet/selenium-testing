import itertools

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

def are_elements_present(driver, *args):
    return len(driver.find_elements(*args)) > 0

def product_page(driver):
    driver.get("http://localhost/litecart/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="box-campaigns"]')))
    if (are_elements_present(driver, By.XPATH, '//div[@id="box-campaigns"]')):

        name = driver.find_element(By.XPATH, '//div[@id="box-campaigns"]//div[@class="name"]').text
        price = driver.find_element(By.XPATH,'//div[@id="box-campaigns"]//div[@class="price-wrapper"]/*[@class="regular-price"]')
        sale_price = driver.find_element(By.XPATH, '//div[@id="box-campaigns"]//div[@class="price-wrapper"]/*[@class="campaign-price"]')
        color_price = price.value_of_css_property("color")
        color_sale_price = sale_price.value_of_css_property("color")
        href = driver.find_element(By.XPATH, '//div[@id="box-campaigns"]/div/ul/li/a').get_attribute("href")

        sale_price_rgb = list(map(int,''.join(itertools.filterfalse(str.isalpha,color_sale_price))[1:-1].split(',')))
        main_price_rgb = list(map(int, ''.join(itertools.filterfalse(str.isalpha,color_price))[1:-1].split(',')))
        assert main_price_rgb[0] == main_price_rgb[1] == main_price_rgb[2], "Color price invalid"
        assert sale_price_rgb[1] == sale_price_rgb[2], "Color sale price invalid"
        assert price.tag_name.lower() == "s", "Price is not strike"
        assert sale_price.tag_name.lower() == "strong", "Price is not strong"
        price_font = ''.join(itertools.filterfalse(str.isalpha,price.value_of_css_property("font-size")))
        sale_price_font = ''.join(itertools.filterfalse(str.isalpha, sale_price.value_of_css_property("font-size")))
        assert float(sale_price_font) > float(price_font), "price not small"
        driver.get(href)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[@itemprop="name"]')))
        if (are_elements_present(driver, By.XPATH, '//h1[@itemprop="name"]')):
            assert driver.find_element(By.XPATH, '//h1[@itemprop="name"]').text == name, "Invalid product name"
            product_page_price = driver.find_element(By.XPATH, '//div[@class="information"]//*[@class="regular-price"]')
            product_page_sale_price = driver.find_element(By.XPATH,'//div[@class="information"]//*[@class="campaign-price"]')
            product_page_color_price = product_page_price.value_of_css_property("color")
            product_page_color_sale_price = product_page_sale_price.value_of_css_property("color")
            sale_price_rgb = list(map(int, ''.join(itertools.filterfalse(str.isalpha, product_page_color_sale_price))[1:-1].split(',')))
            price_rgb = list(map(int, ''.join(itertools.filterfalse(str.isalpha, product_page_color_price))[1:-1].split(',')))
            assert price_rgb[0] == price_rgb[1] == price_rgb[2], "Color price invalid"
            assert sale_price_rgb[1] == sale_price_rgb[2], "Color sale price invalid"
            assert product_page_price.tag_name.lower() == "s", "Price is not strike"
            assert product_page_sale_price.tag_name.lower() == "strong", "Price is not strong"
            price_font = ''.join(itertools.filterfalse(str.isalpha, product_page_price.value_of_css_property("font-size")))
            sale_price_font = ''.join(itertools.filterfalse(str.isalpha, product_page_sale_price.value_of_css_property("font-size")))
            assert float(sale_price_font) > float(price_font), "price not small"

def test_admin_page(driverChrome, driverSafari, driverFirefox):
    product_page(driverChrome)
    product_page(driverSafari)
    product_page(driverFirefox)