"""
Page‑Object for the SauceDemo inventory / product list.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class InventoryPage:
    """Operations on the inventory screen."""
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@id, 'add-to-cart')]")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def add_to_cart(self, product_name: str):
        """Click the Add to Cart button for a given product."""
        # Simple locator; replace with a more robust one later.
        button = self.driver.find_element(
            By.XPATH,
            f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button"
        )
        button.click()

    def go_to_cart(self):
        self.driver.find_element(*self.CART_ICON).click()

    def proceed_to_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()