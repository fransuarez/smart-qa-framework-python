"""
Self‑healing driver wrapper (Healenium or custom fallback).
"""

from typing import Any

class SelfHealingDriver:
    """
    Wrapper that injects Healenium (Docker) into the Selenium/Playwright driver.
    For now it simply forwards attribute access to the underlying driver.
    """
    def __init__(self, driver: Any):
        self.driver = driver
        # TODO: connect to Healenium server if running

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attributes to the wrapped driver."""
        return getattr(self.driver, name)

    # Example of a custom fallback method
    def find_element_with_fallback(self, *args, **kwargs):
        """
        Try the primary locator; if it fails, attempt a secondary strategy.
        """
        try:
            return self.driver.find_element(*args, **kwargs)
        except Exception:
            # TODO: implement fallback logic (e.g., alternative xpath/css)
            raise