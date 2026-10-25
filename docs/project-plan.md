# Definitive Plan: Hybrid Automation Framework + AI

**Repository name:** `smart-qa-framework-python`

**Target applications:**
- **UI target:** [SauceDemo](https://www.saucedemo.com/) — test e‑commerce application
- **API target:** [Fake Store API](https://fakestoreapi.com/) — REST API with JWT authentication and CRUD operations (*)

## Technology stack (100 % free)

| Layer | Technology |
|-------|------------|
| **Language / BDD** | Python 3.11+, `behave` |
| **HTTP / API** | `requests`, `pydantic` (JSON schema validation) |
| **UI** | Playwright **or** Selenium (choose based on team preference) |
| **Visual AI** | Applitools Eyes (Free Starter Plan) |
| **Self‑healing** | Healenium (Docker) **or** custom locator‑fallback logic |
| **Data generation** | Google Gemini API / OpenAI API (free tiers) |
| **CI/CD & reports** | GitHub Actions, Allure Reports, GitHub Pages |

---

## Implementation Plan by Phase

### Phase 1 – Architecture & API Layer (≈ 1 week)

| Goal | Create a robust, reusable HTTP client and BDD scaffolding for the Fake Store API |
|------|-----------------------------------------------------------------------------------|
| **Deliverables** | 1. `features/api_products.feature` – Gherkin scenarios for **auth**, **create**, **read**, **update**, **delete** product endpoints. <br>2. `utils/api_client.py` – Wrapper around `requests` handling: <br> • Base URL & session <br> • JWT acquisition & auto‑refresh <br> • Generic `get/post/put/delete` helpers <br> • Error handling & logging <br>3. `utils/pydantic_models.py` – `Product`, `User`, `AuthResponse` schemas for request/response validation. |
| **Estimated effort** | 2 days – design & skeleton <br>2 days – implementation & unit tests <br>1 day – integrate with `behave` steps |
| **Milestones** | ✅ API client ready <br>✅ First BDD scenarios pass locally |

---

### Phase 2 – UI Layer & Page‑Object Model (≈ 1 week)

| Goal | Automate SauceDemo UI using a clean POM architecture |
|------|--------------------------------------------------------|
| **Deliverables** | 1. `pages/login_page.py` – elements & actions (`login(username, password)`). <br>2. `pages/inventory_page.py` – methods to filter, add‑to‑cart, navigate to checkout. <br>3. `features/ui_checkout.feature` – BDD flow: login → filter → add item → checkout → order confirmation. |
| **Estimated effort** | 1 day – POM scaffolding <br>2 days – implement page methods <br>2 days – BDD steps & first test run <br>1 day – tweak selectors, add basic assertions |
| **Milestones** | ✅ UI tests run end‑to‑end with Playwright/Selenium <br>✅ Allure report generated locally |

---

### Phase 3 – AI Layer Integration (≈ 1‑2 weeks)

| Sub‑module | Description | Key Files | Rough effort |
|------------|-------------|-----------|--------------|
| **LLM Data Generator** | Use Gemini/OpenAI to produce realistic product payloads (including edge‑case values). | `utils/ai_data_generator.py` | 2 days (API wrapper + prompt library) |
| **Visual AI (Applitools)** | Add Applitools Eyes visual checks to the checkout page. | `utils/visual_ai.py` (Eyes init, `check_checkout()`) | 2 days (setup, API key handling, first visual test) |
| **Self‑healing (Healenium)** | Spin up Healenium Docker, integrate with Selenium/Playwright driver. Provide fallback locators when elements shift. | `utils/self_healing.py` (driver wrapper) | 3 days (Docker compose, driver patch, demo scenario) |

**Outcome:** A single BDD scenario will demonstrate: <br>1️⃣ LLM‑generated payload → API POST → schema validation <br>2️⃣ UI login → add known item → checkout → visual AI validation <br>*(No cross‑system data coupling is claimed.)*

---

### Phase 4 – Orchestrated API + UI Demo (≈ 2 days)

| Goal | Combine the three layers into one end‑to‑end BDD story |
|------|-------------------------------------------------------|
| **Feature** | `features/full_flow.feature` – “Generate product → POST to API → Validate → UI checkout → Visual AI check”. |
| **Steps** | - `given` LLM generates payload <br>- `when` API POST executed <br>- `then` response matches `Product` schema <br>- `when` UI login & cart actions <br>- `then` checkout succeeds <br>- `and` Applitools visual check passes |
| **Verification** | Run locally, view Allure + Applitools dashboards, capture screenshots for README. |

---

### Phase 5 – CI/CD, Documentation & Polish (≈ 1 week)

| Deliverable | Details |
|-------------|---------|
| **GitHub Actions** | `.github/workflows/test-pipeline.yml` – steps: <br>1️⃣ Checkout <br>2️⃣ Setup Python 3.11 <br>3️⃣ Install `requirements-dev.txt` <br>4️⃣ Export secrets (`APPLITOOLS_API_KEY`, `GEMINI_API_KEY`) <br>5️⃣ Run `behave -f allure_behave.formatter:AllureFormatter -o allure-results` <br>6️⃣ Publish Allure report as GitHub Pages artifact. |
| **README.md** | - Project overview <br>- Architecture diagram (Mermaid) <br>- Badges for CI status & coverage <br>- How AI is used (LLM data, visual AI, self‑healing) <br>- Screenshots of Applitools & Healenium dashboards <br>- Quick‑start instructions (env file, Docker compose for Healenium). |
| **Documentation** | Update `docs/` with: <br>- `setup.md` (environment & Docker) <br>- `ai-modules.md` (prompt examples, API usage). |
| **Testing** | Add unit tests under `tests/unit/` for: <br>- `api_client` (mocked requests) <br>- `ai_data_generator` (prompt validation) <br>- `visual_ai` (mock Eyes). |
| **Timeline** | Day 1‑2: CI pipeline + README skeleton <br>Day 3‑4: Add diagrams & screenshots <br>Day 5: Final sanity run, bug‑fixes, push to `main`. |

---

## Project Structure (unchanged)

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
│   ├── visual_ai.py
│   └── self_healing.py   # (new)
├── tests/
│   └── unit/
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── README.md