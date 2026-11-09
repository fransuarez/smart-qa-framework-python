# AI Modules Overview

This document explains the two AI‑powered pieces of the framework:

1️⃣ **LLM‑generated test data** – uses OpenAI / Google Gemini to create realistic (and edge‑case) payloads for the Fake Store API.  
2️⃣ **Visual AI with Applitools Eyes** – adds visual‑regression checks to the UI checkout flow.

---  

## 1️⃣ LLM‑Generated Test Data (`utils/ai_data_generator.py`)

The module is a thin wrapper around an LLM API.  
Its responsibilities are:

| Step | What it does |
|------|--------------|
| **Prompt construction** | Builds a clear, constraint‑rich prompt that tells the model what a *product* object should look like. |
| **API call** | Sends the prompt to OpenAI (`openai.ChatCompletion.create`) **or** Google Gemini (`google.generativeai`). The secret key is read from `OPENAI_API_KEY` or `GEMINI_API_KEY`. |
| **Response parsing** | Extracts the JSON block from the raw LLM response and loads it into a Python `dict`. Errors are wrapped in `AIDataError`. |
| **Return value** | A ready‑to‑use dictionary that matches the `Product` Pydantic model defined in `utils/pydantic_models.py`. |

### Prompt example used in the code
```text
You are a test‑data generator for an e‑commerce API.
Create a JSON payload for a new product with the following constraints:
- **title**: a short, catchy name (max 30 characters)
- **price**: a floating‑point number between 0.01 and 9999.99
- **description**: at least 20 words, may include emojis
- **category**: one of ["electronics","jewelery","men's clothing","women's clothing"]
- **image**: a valid URL to a placeholder image (e.g., https://picsum.photos/200)
Return ONLY the JSON object, no extra text.
```

### Example of a generated payload (demo)

```json
{
  "title": "Sleek Lamp",
  "price": 79.99,
  "description": "A modern minimalist lamp that provides warm illumination for any workspace. 🛋️ Perfect for home offices and living rooms.",
  "category": "electronics",
  "image": "https://picsum.photos/200"
}
```

### Expected function signature
```python
def generate_product_payload(prompt: str | None = None) -> dict:
    """
    Calls the LLM, parses the JSON response and returns a dict that
    conforms to the `Product` schema.
    """
```

### Why we generate data with an LLM
* **Variability** – each run can produce a different but valid payload, expanding coverage.  
* **Edge cases** – we can ask the model to intentionally include weird characters, huge numbers, null fields, etc.  
* **Maintainability** – the prompt lives in one place; updating requirements only means editing the prompt, not hand‑crafting many fixtures.

### TODO
- Implement the actual API call for **both** OpenAI and Gemini (choose based on env var).  
- Add retry / back‑off logic for transient LLM errors.  
- Write proper unit tests (see `tests/unit/test_ai_data_generator.py`).  
- Add logging (request/response) for debugging.  

---  

## 2️⃣ Visual AI – Applitools Eyes (`utils/visual_ai.py`)

Applitools provides **AI‑driven visual validation**.  
In the checkout flow we verify that the final confirmation page looks exactly as intended, even if minor CSS changes occur.

### Integration steps (demo)

1. **Initialise Eyes** – reads `APPLITOOLS_API_KEY` from the environment and creates an `Eyes` instance.  
2. **Open a test batch** – `eyes.open(driver, app_name="SmartQA", test_name="checkout_flow")`.  
3. **Capture a snapshot** – `eyes.check_window(tag="checkout_page")`.  
4. **Close & abort** – `eyes.close()` (or `eyes.abort()` on failure).  
5. **Results** – automatically uploaded to the Applitools dashboard where the AI decides if the visual diff is acceptable.

### Minimal usage pattern (copy‑paste into a Behave step)

```python
from utils.visual_ai import VisualAI
import os

def step_impl(context):
    visual = VisualAI(api_key=os.getenv("APPLITOOLS_API_KEY"))
    visual.open(context.driver, app_name="SmartQA", test_name="checkout_flow")
    visual.check_window("checkout_page")
    visual.close()
```

### Example of a successful visual check (demo)

When the step runs, the Applitools dashboard will show something like:

```
[✓] checkout_page – Passed
Baseline: https://eyes.applitools.com/app/tests/baselines/12345
Latest:   https://eyes.applitools.com/app/tests/runs/67890
```

### What the wrapper (`utils/visual_ai.py`) should contain

```python
from applitools.selenium import Eyes, Target

class VisualAI:
    """Thin wrapper around Applitools Eyes for our BDD steps."""
    def __init__(self, api_key: str):
        self.eyes = Eyes()
        self.eyes.api_key = api_key

    def open(self, driver, app_name: str, test_name: str):
        """Start a visual test session."""
        self.eyes.open(driver, app_name=app_name, test_name=test_name)

    def check_window(self, tag: str):
        """Take a full‑page screenshot and let Applitools evaluate it."""
        self.eyes.check(tag, Target.window().fully())

    def close(self):
        """Commit the results to the Applitools server."""
        self.eyes.close()