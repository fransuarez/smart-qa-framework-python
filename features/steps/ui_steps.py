"""
Step definitions for the UI feature files.
"""

from behave import given, when, then
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.visual_ai import VisualAI

@given('the browser is launched')
def step_launch_browser(context):
    # Using Chrome; replace with Playwright if preferred
    context.driver = webdriver.Chrome()
    context.driver.implicitly_wait(5)

@given('the user is on the login page')
def step_open_login(context):
    LoginPage(context.driver).open()

@when('I login with username "{user}" and password "{pwd}"')
def step_login(context, user, pwd):
    LoginPage(context.driver).login(user, pwd)

@when('I add the product "{product_name}" to the cart')
def step_add_product(context, product_name):
    InventoryPage(context.driver).add_to_cart(product_name)

@when('I proceed to the checkout page')
def step_checkout(context):
    InventoryPage(context.driver).go_to_cart()
    InventoryPage(context.driver).proceed_to_checkout()
    # TODO: fill checkout form

@then('the order confirmation page is displayed')
def step_confirm_page(context):
    # Simple assertion – replace with proper check
    assert "checkout-complete" in context.driver.current_url

@then('the visual AI check for the confirmation page passes')
def step_visual_check(context):
    visual = VisualAI(context.driver)
    visual.check_checkout()