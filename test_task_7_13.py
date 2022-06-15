import random
import time
from string import ascii_letters, digits
import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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

def add_products_to_cart(driver):
    driver.get("http://localhost/litecart")
    wait = WebDriverWait(driver,10)
    for i in range(1, 4):
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="box-most-popular"]//a')))
        duck = driver.find_element(By.XPATH, '//div[@id="box-most-popular"]//a')
        duck.click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="box-product"]//h1')))
        if (are_elements_present(driver,By.XPATH, '//*[@id="box-product"]//select')):
            select = Select(driver.find_element(By.XPATH, '//*[@id="box-product"]//select'))
            select.select_by_index(1)
        add_button = driver.find_element(By.XPATH, '//*[@id="box-product"]//button')
        add_button.click()
        stri = str(i)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, '//span[@class="quantity"]'), stri))
        home = driver.find_element(By.XPATH, '//*[@id="breadcrumbs"]//li[1]/a')
        home.click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="box-most-popular"]//a')))
    cart = driver.find_element(By.XPATH, '//*[@id="cart"]/a[3]')
    cart.click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="box-checkout-customer"]/h2')))
    products_ln = len(driver.find_elements(By.XPATH, '//ul[@class="shortcuts"]//a'))

    for i in range(1, products_ln+1):
        if i< products_ln:
            product = driver.find_element(By.XPATH, '//ul[@class="shortcuts"]//a')
            product.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="remove_cart_item"]')))
        name = driver.find_element(By.XPATH,'//a/strong').text
        name_table = driver.find_element(By.XPATH, '//td[contains(text(),"'+name+'")]')
        remove = driver.find_element(By.XPATH, '//button[@name="remove_cart_item"]')
        remove.click()
        wait.until(EC.staleness_of(name_table))

def test_admin_page(driverChrome):
    add_products_to_cart(driverChrome)