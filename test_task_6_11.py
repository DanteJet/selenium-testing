import itertools
import random
import time
from string import ascii_letters, digits

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

def kill_captcha(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    button = driver.find_element(By.NAME, "login")
    button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@id="app-"]')))
    settings = driver.find_element(By.CSS_SELECTOR, "ul.list-vertical li:nth-child(12)")
    settings.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form[@name="settings_form"]')))
    security = driver.find_element(By.XPATH, '//li[@id="doc-security"]')
    security.click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//form[@name="settings_form"]')))
    edit = driver.find_element(By.XPATH, '//table[@class="dataTable"]/tbody/tr[7]/td[3]/a')
    edit.click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//input[@value="0"]')))
    radio = driver.find_element(By.XPATH, '//input[@value="0"]')
    radio.click()
    save_button = driver.find_element(By.XPATH, '//button[@name="save"]')
    save_button.click()

def register_page(driver):
    driver.get("http://localhost/litecart/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="box-campaigns"]')))
    link_reg = driver.find_element(By.XPATH, '//div[@id="box-account-login"]//table//tr[5]//a')
    link_reg.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(((By.XPATH, '//h1[@class="title"]'))))
    first_name = driver.find_element(By.XPATH, '//input[@name="firstname"]')
    first_name.send_keys("Aladdin")
    last_name = driver.find_element(By.XPATH, '//input[@name="lastname"]')
    last_name.send_keys("Aladdinov")
    address1_name = driver.find_element(By.XPATH, '//input[@name="address1"]')
    address1_name.send_keys("Bagdad, Main Street, 345")
    postcode = driver.find_element(By.XPATH, '//input[@name="postcode"]')
    postcode.send_keys("99577")
    city = driver.find_element(By.XPATH, '//input[@name="city"]')
    city.send_keys("Bagdad")
    select_country = Select(driver.find_element(By.XPATH, '//select[@name="country_code"]'))
    select_country.select_by_value("US")
    select_zone = Select(driver.find_element(By.XPATH, '//select[@name="zone_code"]'))
    values= int(len(driver.find_elements(By.XPATH, '//select[@name="zone_code"]/option')))
    values = values-1
    pos = random.randint(0, (values))
    select_zone.select_by_index(pos)
    email = driver.find_element(By.XPATH, '//input[@name="email"]')
    mail = ''.join(random.choice(ascii_letters) for i in range(20))+"@example.com"
    email.send_keys(mail)
    phone = driver.find_element(By.XPATH, '//input[@name="phone"]')
    phone.send_keys(''.join(random.choice(digits) for i in range(14)))
    password = "q1W2e3R4d5"
    passw = driver.find_element(By.XPATH, '//input[@name="password"]')
    passw.send_keys(password)
    passw_conf = driver.find_element(By.XPATH, '//input[@name="confirmed_password"]')
    passw_conf.send_keys(password)
    btn = driver.find_element(By.XPATH, '//button[@name="create_account"]')
    btn.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="box-account"]//ul/li[4]/a')))
    logout = driver.find_element(By.XPATH, '//div[@id="box-account"]//ul/li[4]/a')
    logout.click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//div[@id="box-account-login"]/h3')))
    email_input = driver.find_element(By.XPATH, '//input[@name="email"]')
    email_input.send_keys(mail)
    password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
    password_input.send_keys(password)
    button_login = driver.find_element(By.XPATH, '//button[@name="login"]')
    button_login.click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="box-account"]/h3')))
    logout = driver.find_element(By.XPATH, '//div[@id="box-account"]//ul/li[4]/a')
    logout.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="box-account-login"]/h3')))
def test_admin_page(driverChrome):
    kill_captcha(driverChrome)
    register_page(driverChrome)