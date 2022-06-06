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

def admin_page(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    button = driver.find_element(By.NAME, "login")
    button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@id="app-"]')))
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"table.dataTable tr.row")))
    if (are_elements_present(driver, By.CSS_SELECTOR, "table.dataTable tr.row")):
        countries = driver.find_elements(By.CSS_SELECTOR, "table.dataTable tr.row")
        countrys_href = []
        for country in countries:
            countrys_href.append(country.find_element(By.CSS_SELECTOR, "td:nth-child(3) a").get_attribute("href"))
        print(len(countrys_href))
        for i in range(len(countrys_href)):
            zone_names=[]
            driver.get(countrys_href[i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table-zones>tbody>tr")))
            if (are_elements_present(driver, By.CSS_SELECTOR, "#table-zones>tbody>tr")):
                options = driver.find_elements(By.XPATH, "//td[3]/select/option[@selected='selected']")
                for option in options:
                    zone_names.append(option.text)
                zone_names_sorted = list(zone_names)
                zone_names_sorted.sort()
                assert zone_names_sorted == zone_names, "Sort invalid"

def test_admin_page(driverChrome):
    admin_page(driverChrome)