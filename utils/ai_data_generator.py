"""
Stub for LLM‑driven test‑data generation.
"""

import os
from typing import Dict

# In a real implementation you’d import google‑gemini / openai SDKs.
# Here we just return a static dict as a placeholder.

def generate_product_payload() -> Dict:
    """
    Calls the configured LLM (Gemini/OpenAI) and returns a dict that
    conforms to the ``Product`` schema.
    """
    # TODO: replace with actual API call
    return {
        "title": "AI‑Generated Widget",
        "price": 42.99,
        "description": "A widget created by an LLM for testing edge cases.",
        "category": "electronics",
        "image": "https://example.com/widget.png"
    }