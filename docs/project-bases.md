# Definitive Plan: Hybrid Automation Framework + AI

**Repository name:** `smart-qa-framework-python`

**Target applications:**

- **UI target:** [SauceDemo](https://www.saucedemo.com/) — test e-commerce application
- **API target:** [Fake Store API](https://fakestoreapi.com/) — REST API with JWT authentication and CRUD operations (*)

## Technology stack (100% free)

- **Language and BDD:** Python 3.11+ / `behave`
- **HTTP/API layer:** `requests` / `pydantic` for JSON schema validation
- **UI layer:** Playwright or Selenium
- **AI module 1 — Visual AI:** Applitools Eyes (*Free Starter Plan*)
- **AI module 2 — Self-healing:** Healenium (via Docker) or AI-assisted alternative locator strategies
- **AI module 3 — Data generation:** Google Gemini API / OpenAI API (free tiers)
- **CI/CD and reports:** GitHub Actions + Allure Reports / GitHub Pages

## Implementation plan by phase

### Phase 1: Architecture and backend (API) layer

- **Goal:** Create the Python HTTP client and configure BDD for the backend.
- **Deliverables:**
  1. Create `features/api_products.feature` with Gherkin BDD scenarios for creating and retrieving products, and authenticating users in the *Fake Store API*.
  2. Implement `utils/api_client.py`, a Python module using `requests` to handle GET, POST, PUT, and DELETE requests, as well as JWT tokens.
  3. Add JSON schema validation with `pydantic` to ensure backend data integrity.

### Phase 2: Frontend (UI) layer and Page Object Model

- **Goal:** Automate the web interface using the Page Object Model (POM) design pattern.
- **Deliverables:**
  1. Create `pages/login_page.py` and `pages/inventory_page.py` to map the elements on *SauceDemo*.
  2. Create `features/ui_checkout.feature` to automate login, item filtering, the cart, and checkout.

### Phase 3: Integrate the AI layer

#### 1. LLM data generator (`utils/ai_data_generator.py`)

Use the Gemini API or another LLM to dynamically generate realistic product payloads or user data, including edge cases, instead of relying on hardcoded data.

#### 2. Visual AI module with Applitools (`utils/visual_ai.py`)

- Integrate Applitools Eyes into the *SauceDemo* checkout test.
- Configure a full UI check (`eyes.check("Checkout Page")`) to demonstrate how AI can detect layout shifts or visual defects that traditional assertions might miss.

#### 3. Self-healing module

Configure Healenium in the project so that UI tests can tolerate DOM attribute changes at runtime.

### Phase 4: Orchestrated API and UI Demo

- **Goal:** Demonstrate API testing, UI testing, and visual AI in one BDD scenario without implying that Fake Store API data appears in SauceDemo.
- **Flow:**
  1. `Given`: The LLM generates a valid product payload.
  2. `When`: The test sends the payload to Fake Store API with a POST request.
  3. `Then`: Validate the response against the product schema and check the returned fields. Treat the write as simulated; do not assume it persists.
  4. `When`: The test independently logs in to SauceDemo and adds a known inventory item to the cart.
  5. `Then`: Validate the SauceDemo checkout flow and use Applitools to check the final UI screen.
- **Note:** The API product and SauceDemo inventory item are separate test data. No assertion should claim that the API-created product appears in SauceDemo.

### Phase 5: GitHub Actions CI/CD pipeline and documentation

- **Goal:** Set up continuous automation and prepare the project for an interview.
- **Deliverables:**
  1. `.github/workflows/test-pipeline.yml`: A pipeline that installs dependencies, runs `behave`, and generates the report.
  2. A professional `README.md` containing:
     - A framework architecture diagram using Mermaid.js.
     - GitHub Actions build badges.
     - A clear explanation of why and how AI was applied in the project.
     - Screenshots showing the Applitools / Healenium dashboards in action.

## Project Structure

```
smart-qa-framework-python/          # Repository root
├── .github/
│   └── workflows/
│       └── test-pipeline.yml      # GitHub Actions CI/CD
├── docs/
│   └── project-plan.md            # This definitive plan
├── features/
│   ├── api_products.feature       # BDD scenarios for Fake Store API
│   ├── ui_checkout.feature        # BDD scenarios for SauceDemo UI flow
│   └── steps/                     # Step‑definition modules
│       ├── api_steps.py
│       └── ui_steps.py
├── pages/
│   ├── login_page.py              # Page‑Object for SauceDemo login
│   └── inventory_page.py          # Page‑Object for product listing & cart
├── utils/
│   ├── api_client.py              # HTTP client (requests + JWT handling)
│   ├── ai_data_generator.py       # LLM‑driven payload generator
│   └── visual_ai.py               # Applitools Eyes integration
├── tests/
│   └── unit/                      # Unit tests for utils & client code
├── requirements.txt               # Production dependencies
├── requirements-dev.txt           # Dev / testing dependencies (behave, allure, etc.)
├── .env.example                   # Sample environment file
└── README.md                      # Project overview (generated from this plan)
```
