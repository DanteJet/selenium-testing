from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LitecartCartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)

    def open(self):
        self.driver.get("http://localhost/litecart/en/checkout")
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="customer-service-wrapper"]/span')))
        return self

    def delete_product(self):
        assert len(self.driver.find_elements(By.XPATH, '//*[@id="checkout-cart-wrapper"]/p/em'))==0, "No products in cart"
        if len(self.driver.find_elements(By.XPATH, '//ul[@class="shortcuts"]//a'))>0:
            product = self.driver.find_element(By.XPATH, '//ul[@class="shortcuts"]//a')
            product.click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="remove_cart_item"]')))
        name = self.driver.find_element(By.XPATH, '//a/strong').text
        name_table = self.driver.find_element(By.XPATH, '//td[contains(text(),"' + name + '")]')
        remove = self.driver.find_element(By.XPATH, '//button[@name="remove_cart_item"]')
        remove.click()
        self.wait.until(EC.staleness_of(name_table))

    def are_elements_present(self, *args):
        return len(self.driver.find_elements(*args)) > 0

    def get_product_type_count(self):
        count = 0
        if(self.are_elements_present(By.XPATH, '//ul[@class="shortcuts"]//a')):
            count = len(self.driver.find_elements(By.XPATH, '//ul[@class="shortcuts"]//a'))
        elif(len(self.driver.find_elements(By.XPATH, '//*[@id="checkout-cart-wrapper"]/p/em'))==0):
            count=1
        return count