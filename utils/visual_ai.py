"""
Thin wrapper around Applitools Eyes.
"""

import os
from applitools.selenium import Eyes, Target  # or applitools.playwright

class VisualAI:
    """Initialize Eyes and perform a visual checkpoint on the checkout page."""
    def __init__(self, driver):
        self.eyes = Eyes()
        self.eyes.api_key = os.getenv("APPLITOOLS_API_KEY")
        self.driver = driver

    def check_checkout(self) -> None:
        """Run a visual validation of the checkout confirmation screen."""
        # TODO: adapt to Selenium or Playwright driver
        self.eyes.open(self.driver, "SauceDemo", "Checkout")
        self.eyes.check("Checkout Confirmation", Target.window())
        self.eyes.close()