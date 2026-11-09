# Hybrid Automation Framework - Original Architecture Plan

**Repository name:** `smart-qa-framework-python`

**Target applications:**
- **UI target:** [SauceDemo](https://www.saucedemo.com/) — test e-commerce application
- **API target:** [Fake Store API](https://fakestoreapi.com/) — REST API with JWT authentication and CRUD operations

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
  1. Create `features/api_products.feature` with Gherkin BDD scenarios for creating and retrieving products, and authenticating users in the Fake Store API.
  2. Implement `utils/api_client.py`, a Python module using `requests` to handle GET, POST, PUT, and DELETE requests, as well as JWT tokens.
  3. Add JSON schema validation with `pydantic` to ensure backend data integrity.

### Phase 2: Frontend (UI) layer and Page Object Model
- **Goal:** Automate the web interface using the Page Object Model (POM) design pattern.
- **Deliverables:**
  1. Create `pages/login_page.py` and `pages/inventory_page.py` to map the elements on SauceDemo.
  2. Create `features/ui_checkout.feature` to automate login, item filtering, the cart, and checkout.

### Phase 3: Integrate the AI layer
- **LLM data generator** (`utils/ai_data_generator.py`) — Gemini/OpenAI payload generation
- **Visual AI module** (`utils/visual_ai.py`) — Applitools Eyes checkout validation
- **Self-healing module** — Healenium Docker integration

### Phase 4: Orchestrated API and UI Demo
- **Goal:** Demonstrate API testing, UI testing, and visual AI in one BDD scenario.
- **Flow:** LLM payload → Fake Store API → Validation → SauceDemo checkout → Visual AI

### Phase 5: GitHub Actions CI/CD pipeline and documentation
- **Deliverables:** Complete CI pipeline, professional README with Mermaid diagram and Applitools screenshots

## Project Structure
```
smart-qa-framework-python/
├── .github/
│   └── workflows/
│       └── test-pipeline.yml
├── docs/
│   └── project-plan.md
├── features/
│   ├── api_products.feature
│   ├── ui_checkout.feature
│   └── steps/
│       ├── api_steps.py
│       └── ui_steps.py
├── pages/
│   ├── login_page.py
│   └── inventory_page.py
├── utils/
│   ├── api_client.py
│   ├── ai_data_generator.py
│   └── visual_ai.py
├── tests/
│   └── unit/
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── README.md
```
```

### **`docs/project-plan.md` - Current Implementation Status** (Your updated version)

```markdown
# Definitive Plan: Hybrid Automation Framework + AI

**Repository name:** `smart-qa-framework-python`

**Target applications:**
- **UI target:** [`flask-shop-demo`](https://github.com/fransuarez/flask-shop-demo) — thin Flask + Jinja frontend (session cart, no DB)
- **API target:** [Fake Store API](https직접 (https://fakestoreapi.com/) — read-only product catalog (no JWT/auth needed)

## Current Implementation Status

**Significant Progress Made:**
- ✅ Full BDD framework implemented (api_products.feature, ui_checkout.feature, steps/)
- ✅ Complete API client with validation (no JWT needed)
- ✅ AI modules integrated (data generation, visual AI, self-healing)
- ✅ CI/CD pipeline operational (GitHub Actions)
- ✅ Unit tests for key components
- ✅ Requirements management setup

**Critical Architecture Mismatch:**
- **Plans:** SauceDemo UI target
- **Reality:** flask-shop-demo UI target (session cart, no login required)
- **Impact:** Page objects and BDD scenarios require re-alignment

**Immediate Action Items:**
1. **Realign UI target** - Fix page objects for flask-shop-demo `data-testid` hooks
2. **Complete page object model** - Add cart_page.py, checkout_page.py, base_page.py
3. **Add standard files** - .env.example, LICENSE, requirements-dev.txt
4. **Complete documentation** - Add docs/context.md
5. **Fix implementation** - Remove SauceDemo references

## Project Structure (Current Reality)
```
smart-qa-framework-python/
├── .github/
│   └── workflows/
│       └── test-pipeline.yml           ✅ exists
├── docs/
│   ├── project-plan.md                ✅ current status
│   ├── project-bases.md               ✅ original architecture
│   ├── context.md                   ⚠️ missing
│   ├── setup.md                      ✅ exists
│   └── ai-modules.md                 ✅ exists
├── features/
│   ├── api_products.feature          ✅ exists
│   ├── ui_checkout.feature           ✅ exists
│   ├── full_flow.feature             ✅ exists
│   └── steps/
│       ├── api_steps.py              ✅ exists
│       └── ui_steps.py               ✅ exists
├── pages/
│   ├── login_page.py                 ⚠️ exists but unused (flask-shop-demo no login)
│   └── inventory_page.py             ✅ exists for flask-shop-demo
├── utils/
│   ├── api_client.py                 ✅ implemented
│   ├── pydantic_models.py            ✅ implemented
│   ├── ai_data_generator.py          ✅ implemented
│   ├── visual_ai.py                  ✅ implemented
│   └── self_healing.py               ✅ implemented
├── tests/
│   └── unit/
│       ├── __init__.py               ✅ exists
│       ├── test_api_client.py        ✅ exists
│       └── test_ai_data_generator.py ✅ exists
├── requirements.txt                  ✅ exists
├── resources/
│   └── fake-store-api/
│       └── fakestore-api-doc.json   ✅ exists
├── behave.ini                        ✅ exists
├── .gitignore                        ✅ exists
└── README.md                         ✅ exists
```