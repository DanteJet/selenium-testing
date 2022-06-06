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

def product_page(driver):
    driver.get("http://localhost/litecart/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="box-campaigns"]')))
    if (are_elements_present(driver, By.XPATH, '//div[@id="box-campaigns"]')):

        name = driver.find_element(By.XPATH, '//div[@id="box-campaigns"]//div[@class="name"]').text
        price = driver.find_element(By.XPATH,'//div[@id="box-campaigns"]//div[@class="price-wrapper"]/*[@class="regular-price"]')
        price_text = price.text
        sale_price = driver.find_element(By.XPATH, '//div[@id="box-campaigns"]//div[@class="price-wrapper"]/*[@class="campaign-price"]')
        sale_price_text = sale_price.text
        color_price = price.value_of_css_property("color")
        color_sale_price = sale_price.value_of_css_property("color")
        href = driver.find_element(By.XPATH, '//div[@id="box-campaigns"]/div/ul/li/a').get_attribute("href")
        main_price_rgb = "rgba(119, 119, 119, 1)"
        sale_price_rgb = "rgba(204, 0, 0, 1)"
        assert color_price == main_price_rgb, "Color price invalid"
        assert color_sale_price == sale_price_rgb, "Color sale price invalid"
        assert price.tag_name == "s", "Price is not strike"
        assert sale_price.tag_name == "strong", "Price is not strong"
        assert (sale_price.size["height"] > price.size["height"]) & (sale_price.size["width"] > price.size["width"]), "sale price smaller"
        driver.get(href)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[@itemprop="name"]')))
        if (are_elements_present(driver, By.XPATH, '//h1[@itemprop="name"]')):
            product_page_color_price_rgb = "rgba(102, 102, 102, 1)"
            assert driver.find_element(By.XPATH, '//h1[@itemprop="name"]').text == name, "Invalid product name"
            product_page_price = driver.find_element(By.XPATH, '//div[@class="information"]//*[@class="regular-price"]')
            product_page_sale_price = driver.find_element(By.XPATH,'//div[@class="information"]//*[@class="campaign-price"]')
            product_page_color_price = product_page_price.value_of_css_property("color")
            product_page_color_sale_price = product_page_sale_price.value_of_css_property("color")
            assert product_page_color_price == product_page_color_price_rgb, "Color price invalid"
            assert product_page_color_sale_price == sale_price_rgb, "Color sale price invalid"
            assert product_page_price.tag_name == "s", "Price is not strike"
            assert product_page_sale_price.tag_name == "strong", "Price is not strong"
            assert (product_page_sale_price.size["height"] > product_page_price.size["height"]) & (
                        product_page_sale_price.size["width"] > product_page_price.size["width"]), "sale price smaller"





def test_admin_page(driverChrome):
    product_page(driverChrome)