import random
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

def delete_product(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    button = driver.find_element(By.NAME, "login")
    button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@id="app-"]')))
    catalog = driver.find_element(By.CSS_SELECTOR, "ul.list-vertical li:nth-child(2)")
    catalog.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/a[2]')))
    names = driver.find_elements(By.XPATH, '//*[@id="content"]/form/table/tbody/tr/td[3]')
    for name in names:
        if name.text == "Cute duck":
            edit = name.find_element(By.CSS_SELECTOR, 'i.fa-pencil')
            edit.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@name="delete"]')))
            del_btn = driver.find_element(By.XPATH, '//button[@name="delete"]')
            del_btn.click()
def add_product(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    button = driver.find_element(By.NAME, "login")
    button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@id="app-"]')))
    catalog = driver.find_element(By.CSS_SELECTOR, "ul.list-vertical li:nth-child(2)")
    catalog.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/a[2]')))
    button_add = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/a[2]')
    button_add.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-general"]/table')))
    radio_button = driver.find_element(By.XPATH,'//*[@id="tab-general"]/table/tbody/tr[1]//input[@value="1"]')
    radio_button.click()
    name = driver.find_element(By.XPATH, '//*[@name="name[en]"]')
    name_text = mail = ''.join(random.choice(ascii_letters) for i in range(22))+" rubber duck"
    name.send_keys(name_text)
    code = driver.find_element(By.XPATH, '//*[@name="code"]')
    code.send_keys("cd456")
    rbd_check = driver.find_element(By.XPATH, '//*[@id="tab-general"]//tr[4]//tr[2]/td[1]/input')
    rbd_check.click()
    category_select = Select(driver.find_element(By.XPATH, '//*[@name="default_category_id"]'))
    category_select.select_by_index(1)
    pg_value = driver.find_element(By.XPATH, '//input[@value="1-3"]')
    pg_value.click()
    quantity = driver.find_element(By.XPATH, '//input[@name="quantity"]')
    quantity.clear()
    quantity.send_keys("123")
    upload_button = driver.find_element(By.XPATH, '//input[@name="new_images[]"]')
    upload_button.send_keys(os.path.abspath('duck.jpeg'))
    date_valid_from = driver.find_element(By.XPATH, '//input[@name="date_valid_from"]')
    date_valid_from.send_keys("01012012")
    date_valid_to = driver.find_element(By.XPATH, '//input[@name="date_valid_to"]')
    date_valid_to.send_keys("01122099")
    information = driver.find_element(By.XPATH, '//div[@class="tabs"]//li[2]')
    information.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//select[@name="manufacturer_id"]')))
    mnf_id = Select(driver.find_element(By.XPATH, '//select[@name="manufacturer_id"]'))
    mnf_id.select_by_index(1)
    keywords = driver.find_element(By.XPATH, '//input[@name="keywords"]')
    keywords.send_keys("duck, rubber duck, sweat, cute, cool")
    short_desc = driver.find_element(By.XPATH, '//input[@name="short_description[en]"]')
    short_desc.send_keys("Cute duck")
    desc = driver.find_element(By.XPATH, '//textarea[@name="description[en]"]')
    desc.send_keys("Small cute rubber duck with sunglasses")
    headtitle = driver.find_element(By.XPATH, '//input[@name="head_title[en]"]')
    headtitle.send_keys("cute duck")
    meta_desc = driver.find_element(By.XPATH, '//input[@name="meta_description[en]"]')
    meta_desc.send_keys("duck")
    prices = driver.find_element(By.XPATH, '//div[@class="tabs"]//li[4]')
    prices.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="purchase_price"]')))
    purch_price = driver.find_element(By.XPATH, '//input[@name="purchase_price"]')
    purch_price.clear()
    purch_price.send_keys("44")
    purch_select = Select(driver.find_element(By.XPATH, '//select[@name="purchase_price_currency_code"]'))
    purch_select.select_by_index(1)
    usd = driver.find_element(By.XPATH, '//input[@name="gross_prices[USD]"]')
    usd.clear()
    usd.send_keys("44")
    eur = driver.find_element(By.XPATH, '//input[@name="gross_prices[EUR]"]')
    eur.clear()
    eur.send_keys("53")
    save_btn = driver.find_element(By.XPATH, '//button[@name="save"]')
    save_btn.click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="notices"]/div')))
    rb_ducks = driver.find_element(By.XPATH, '//*[@id="content"]/form//tr[3]/td[3]/a')
    rb_ducks.click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/form/table/tbody/tr/td[3]')))
    names = driver.find_elements(By.XPATH, '//*[@id="content"]/form/table/tbody/tr/td[3]')
    nm=0
    for name in names:
        if name.text == name_text:
            nm = 1
    assert nm >= 1, "oops, product not found"

def test_admin_page(driverChrome):
    add_product(driverChrome)