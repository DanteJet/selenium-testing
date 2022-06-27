from selenium import webdriver
from pages.litecart_cart_page import LitecartCartPage
from pages.litecart_main_page import LitecartMainPage
from pages.litecart_product_page import LitecartProductPage

class Application:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.main_page = LitecartMainPage(self.driver)
        self.product_page = LitecartProductPage(self.driver)
        self.cart_page = LitecartCartPage(self.driver)

    def quit(self):
        self.driver.quit()

    def add_first_product_to_cart(self):
        self.main_page.open()
        link = self.main_page.get_first_product_link()
        self.product_page.open(link)
        self.product_page.add_product_to_cart()

    def delete_product_from_cart(self):
        self.cart_page.open()
        self.cart_page.delete_product()

    def check_no_product_in_cart(self):
        self.main_page.open()
        if self.main_page.get_product_count()==0:
            return True
        else:
            return False

    def get_count_product_cards_in_cart(self):
        self.cart_page.open()
        return self.cart_page.get_product_type_count()
