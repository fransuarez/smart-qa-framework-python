# Smart QA Framework – Python

![CI Status](https://img.shields.io/github/actions/workflow/status/your‑repo/smart-qa-framework-python/test-pipeline.yml?branch=main)

## Overview
A hybrid **API + UI** test automation framework built with **behave**, **Playwright/Selenium**, **LLM‑generated test data**, **Applitools Eyes**, and **Healenium** self‑healing.

## Quick‑Start
```bash
# 1️⃣ Clone & cd
git clone https://github.com/your‑repo/smart-qa-framework-python.git
cd smart-qa-framework-python

# 2️⃣ Install Python deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3️⃣ (Optional) Start Healenium via Docker‑compose
docker-compose -f docker/healenium.yml up -d

# 4️⃣ Run BDD tests
behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

## Project Structure
*(see the repository tree for details)*

## Documentation
- **Setup** – `docs/setup.md`  
- **AI Modules** – `docs/ai-modules.md`  

## TODO
- Add architecture diagram (Mermaid)  
- Add badge for test coverage  
- Populate usage examples and screenshots  

--- 

*(Feel free to flesh out each section as the project evolves.)*

```

---

### `docs/setup.md` – environment & Docker‑compose instructions (placeholder)

```markdown docs/setup.md
# Setup Guide

## Prerequisites
- Python 3.11+
- Docker & Docker‑Compose (for Healenium)
- Git
- (Optional) OpenAI / Google Gemini API keys
- (Optional) Applitools API key

## 1️⃣ Clone the repository
```bash
git clone https://github.com/your‑repo/smart-qa-framework-python.git
cd smart-qa-framework-python
```

## 2️⃣ Python environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 3️⃣ Healenium (self‑healing) – Docker Compose
```yaml
# docker/healenium.yml (example)
version: "3.8"
services:
  healenium:
    image: seleniumhq/healenium:latest
    ports:
      - "8080:8080"
    environment:
      - SELENIUM_HOST=selenium
      - SELENIUM_PORT=4444
```

```bash
docker-compose -f docker/healenium.yml up -d
# Verify: http://localhost:8080/healthcheck
```

## 4️⃣ Environment variables
Copy `.env.example` to `.env` and fill in the secrets:

```bash
cp .env.example .env
# Edit .env:
# APPLITOOLS_API_KEY=your_key
# GEMINI_API_KEY=your_key
# OPENAI_API_KEY=your_key
```

## 5️⃣ Running the test suite
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

## 6️⃣ Generating the Allure report locally
```bash
npm install -g allure-commandline --save-dev   # if not already installed
allure serve allure-results
```

---

* Further sections (e.g., troubleshooting, CI integration) can be added as the project matures.*
```

---

### `docs/ai-modules.md` – LLM & Applitools integration overview (placeholder)

```markdown docs/ai-modules.md
# AI Modules Overview

## 1️⃣ LLM‑Generated Test Data (`utils/ai_data_generator.py`)

The module talks to **OpenAI** or **Google Gemini** to synthesize realistic product payloads, including edge‑case values (negative prices, very long titles, special characters, etc.).

### Prompt example
```text
You are a test‑data generator for an e‑commerce API. Produce a JSON payload for a new product with the following constraints:
- title: a short, catchy name (max 30 characters)
- price: a floating‑point number between 0.01 and 9999.99
- description: at least 20 words, may include emojis
- category: one of ["electronics","jewelery","men's clothing","women's clothing"]
- image: a valid URL to a placeholder image
```

The function `generate_product_payload()` sends this prompt, receives the raw text, parses it into a Python `dict`, and returns it for the API test step.

---

## 2️⃣ Visual AI – Applitools Eyes (`utils/visual_ai.py`)

Applitools provides **visual regression** checks. In the UI flow we:

1. Initialise an `Eyes` instance with the API key from `APPLITOOLS_API_KEY`.
2. Open a test batch (`checkout_flow`).
3. Call `eyes.check_window(tag="checkout_page")` after the order‑confirmation screen.
4. Close the session and push results to the Applitools dashboard.

### Minimal usage pattern
```python
from utils.visual_ai import VisualAI

visual = VisualAI(api_key=os.getenv("APPLITOOLS_API_KEY"))
visual.open(driver, "Checkout Flow")
visual.check_window("checkout_page")
visual.close()
```

---

## 3️⃣ Self‑Healing (Healenium)

Healenium runs as a Docker service that intercepts Selenium/Playwright commands. When a locator fails, Healenium queries its internal fallback map and retries with an alternative selector. Integration is handled in `utils/self_healing.py` by wrapping the driver creation:

```python
from selenium import webdriver

def get_healenium_driver():
    options = webdriver.ChromeOptions()
    # Healenium proxy configuration
    options.add_argument("--proxy-server=http://localhost:8080")
    return webdriver.Chrome(options=options)
```

---
