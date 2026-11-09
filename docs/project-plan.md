# Definitive Plan: Hybrid Automation Framework + AI

**Repository name:** `smart-qa-framework-python`

**Target applications:**
- **UI target:** [`flask-shop-demo`](https://github.com/fransuarez/flask-shop-demo) — thin Flask + Jinja frontend (session cart, no DB)
- **API target:** [Fake Store API](https://fakestoreapi.com/) — read-only product catalog (no JWT/auth needed)

## Technology stack (100% free)

| Layer | Technology |
|-------|------------|
| **Language / BDD** | Python 3.11+, `behave` |
| **HTTP / API** | `requests`, `pydantic` (JSON schema validation) |
| **UI** | Playwright (current implementation) **or** Selenium |
| **Visual AI** | Applitools Eyes (Free Starter Plan) ✅ **IMPLEMENTED** |
| **Self‑healing** | Healenium (Docker) ✅ **IMPLEMENTED** |
| **Data generation** | Google Gemini API / OpenAI API ✅ **IMPLEMENTED** |
| **CI/CD & reports** | GitHub Actions, Allure Reports, GitHub Pages ✅ **IMPLEMENTED** |

---

## Implementation Plan by Phase

### Phase 1 – Architecture & API Layer ✅ **IMPLEMENTED**

| Goal | Create a robust, reusable HTTP client and BDD scaffolding for Fake Store catalog validation |
|------|-----------------------------------------------------------------------------------|
| **Status** | ✅ **COMPLETED** |
| **Deliverables** |  Subaru **updated**:
   - `features/api_products.feature` ✅ (catalog validation scenarios)
   - `utils/api_client.py` ✅ (public API client, no JWT needed)
   - `utils/pydantic_models.py` ✅ (Product schema for catalog validation)
- **Estimated effort** | 2 days – design & skeleton <br>2 days – implementation & unit tests <br>1 day – integrate with `behave` steps |
| **Milestones** | ✅ API client ready <br>✅ First BDD scenarios pass locally <br>✅ Unit tests for client implementation |

---

### Phase 2 – UI Layer & Page‑Object Model ✅ **IMPLEMENTED (with adjustments)**

| Goal | Automate Flask frontend using POM keyed on verified `data-testid` hooks |
|------|--------------------------------------------------------------------------|
| **Status** | ⚠️ **IMPLEMENTED BUT REQUIRES ALIGNMENT** |
| **Deliverables** | **Current implementation** (needs adjustment to match actual UI target):
   - Page objects (`pages/login_page.py`, `pages/inventory_page.py`) ✅ **exist but need re-alignment**
   - BDD scenarios (`features/ui_checkout.feature`, `features/full_flow.feature`) ✅ **exist but may target wrong application**
   - Step definitions (`features/steps/api_steps.py`, `features/steps/ui_steps.py`) ✅ **exist but may need selector updates**
| **Critical Adjustment Needed** | - Update page objects to use flask-shop-demo `data-testid` contract <br>- Fix BDD scenarios to work with session cart (no login required) <br>- Remove SauceDemo-specific logic from current implementation |
| **Estimated effort** | **Phase 2A (High Priority)**: <br>1 day – realign page objects to flask-shop-demo <br>2 days – update step definitions with correct selectors <br>1 day – adjust BDD scenarios to match actual UI behavior <br>**Phase 2B (Later)**: <br>Add missing page objects (`cart_page.py`, `checkout_page.py`, `base_page.py`) |
| **Milestones** | ✅ UI tests run with correct selectors <br>✅ Allure report generated <br>✅ Session-based test isolation verified |

---

### Phase 3 – AI Layer Integration ✅ **IMPLEMENTED**

| Sub‑module | Status | Key Files |
|------------|--------|-----------|
| **LLM Data Generator** | ✅ **IMPLEMENTED** | `utils/ai_data_generator.py` |
| **Visual AI (Applitools)** | ✅ **IMPLEMENTED** | `utils/visual_ai.py` |
| **Self‑healing (Healenium)** | ✅ **IMPLEMENTED** | `utils/self_healing.py` |

**Current Outcome:** Single BDD scenario (`features/full_flow.feature`) demonstrates API-direct + UI checkout + Visual AI using **current flask-shop-demo** implementation.

---

### Phase 4 – Orchestrated Hybrid Demo ✅ **IMPLEMENTED**

| Goal | Combine API-direct, UI, and Visual AI into one end‑to‑end BDD story |
|------|-------------------------------------------------------------------|
| **Status** | ✅ **COMPLETED** |
| **Feature** | `features/full_flow.feature` ✅ – "LLM ID → API catalog → UI add‑to‑cart → checkout → Visual AI" |
| **Current Implementation** | Uses **flask-shop-demo** (session cart, re-fetched catalog validation) |
| **Verification** | Run locally → Allure + Applitools dashboards → Confirm hybrid guarantee |

---

### Phase 5 – CI/CD, Documentation & Polish ✅ **IMPLEMENTED**

| Deliverable | Status |
|-------------|--------|
| **GitHub Actions** | ✅ `.github/workflows/test-pipeline.yml` ✅ exists |
| **README.md** | ✅ Updated to reflect current implementation (flask-shop-demo) |
| **Documentation** | ✅ `docs/` directory with setup, ai-modules |
| **Testing** | ✅ Unit tests for utils (`tests/unit/test_api_client.py`, `tests/unit/test_ai_data_generator.py`) |
| **Missing Items** | - Missing `.env.example` <br>- Missing `LICENSE` <br>- Missing `requirements-dev.txt` |
| **Timeline** | CI pipeline + Allure setup complete <br>Documentation updated <br>Standard project files needed |

---

## 📊 **Current Repository Status**

### **✅ Implemented (Ahead of Plan)**
- Full BDD framework (`api_products.feature`, `ui_checkout.feature`, `steps/`)
- Complete API client with validation
- AI modules (data generation, visual AI, self-healing)
- CI/CD pipeline with GitHub Actions
- Unit tests for key components

### **⚠️ Needs Adjustment**
- Page objects (`login_page.py` is unused - flask-shop-demo has no login)
- BDD scenarios may target wrong application
- Missing several planned files (`context.md`, `.env.example`, `LICENSE`)

### **📋 Remaining Tasks**
1. **Align UI target** - fix page objects and scenarios for flask-shop-demo
2. **Complete page object model** - add missing `cart_page.py`, `checkout_page.py`, `base_page.py`
3. **Add standard project files** - `.env.example`, `LICENSE`, `requirements-dev.txt`
4. **Update documentation** - complete `docs/context.md`
5. **Fix architecture mismatch** - remove SauceDemo references from current implementation

---

## 🔄 **Project Structure (Updated Reality)**

```
smart-qa-framework-python/
├── .github/
│   └── workflows/
│       └── test-pipeline.yml           ✅ exists
├── docs/
│   ├── project-plan.md                ✅ updated (this file)
│   ├── project-bases.md               ✅ updated (separate file)
│   ├── context.md                    ⚠️ missing
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
│       └── fakestore-api-doc.json    ✅ exists
├── behave.ini                        ✅ exists
├── .gitignore                        ✅ exists
└── README.md                         ✅ exists