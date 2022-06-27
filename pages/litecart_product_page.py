from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LitecartProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, link):
        self.driver.get(link)
        return self

    def are_elements_present(self, *args):
        return len(self.driver.find_elements(*args)) > 0

    def get_product_count(self):
        count = 0
        if(self.are_elements_present(By.XPATH, '//span[@class="quantity"]')):
            count = int(self.driver.find_element(By.XPATH, '//span[@class="quantity"]').text)
        return count


    def add_product_to_cart(self):
        if (self.are_elements_present(By.XPATH, '//*[@id="box-product"]//select')):
            select = Select(self.driver.find_element(By.XPATH, '//*[@id="box-product"]//select'))
            select.select_by_index(1)
        add_button = self.driver.find_element(By.XPATH, '//*[@id="box-product"]//button')
        add_button.click()
        count = self.get_product_count() + 1
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, '//span[@class="quantity"]'), str(count)))

