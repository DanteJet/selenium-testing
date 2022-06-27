from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LitecartMainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)

    def open(self):
        self.driver.get("http://localhost/litecart/en/")
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="box-most-popular"]/h3')))
        return self

    def get_first_product_link(self):
        link = self.driver.find_element(By.XPATH, '//div[@id="box-most-popular"]//a')
        return link.get_attribute("href")

    def are_elements_present(self, *args):
        return len(self.driver.find_elements(*args)) > 0

    def get_product_count(self):
        count = 0
        if(self.are_elements_present(By.XPATH, '//span[@class="quantity"]')):
            count = int(self.driver.find_element(By.XPATH, '//span[@class="quantity"]').text)
        return count