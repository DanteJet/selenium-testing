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
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"tr.row")))
    if (are_elements_present(driver, By.CSS_SELECTOR, "tr.row")):
        countries = driver.find_elements(By.CSS_SELECTOR, "tr.row")
        country_names=[]
        countrys_href = []
        for country in countries:
            country_names.append(country.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text)
            if int(country.find_element(By.CSS_SELECTOR,"td:nth-child(6)").text)>0:
                countrys_href.append(country.find_element(By.CSS_SELECTOR, "td:nth-child(5) a").get_attribute("href"))
        country_names_sorted = list(country_names)
        country_names_sorted.sort()
        assert country_names_sorted == country_names, "Sort invalid"
        for i in range(len(countrys_href)):
            driver.get(countrys_href[i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table-zones>tbody>tr")))
            if (are_elements_present(driver, By.CSS_SELECTOR, "#table-zones>tbody>tr")):
                zones = driver.find_elements(By.CSS_SELECTOR, "#table-zones>tbody>tr")
                zone_names=[]
                for zone in zones:
                    if zone.get_attribute("class")!="header":
                        if len(zone.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text)>0:
                            zone_names.append(zone.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text)
                zone_names_sorted = list(zone_names)
                zone_names_sorted.sort()
                assert zone_names_sorted == zone_names, "Sort invalid"

def test_admin_page(driverChrome):
    admin_page(driverChrome)