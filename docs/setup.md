# Setup Guide

## 📋 Prerequisites
- **Python 3.11+**
- **Docker & Docker‑Compose** (required for Healenium)
- **Git**
- (Optional) API keys for:
  - OpenAI / Google Gemini
  - Applitools Eyes

## 1️⃣ Clone the repository
```bash
git clone https://github.com/your‑repo/smart-qa-framework-python.git
cd smart-qa-framework-python
```

## 2️⃣ Python virtual environment
```bash
python -m venv .venv
# Activate:
#   macOS / Linux: source .venv/bin/activate
#   Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 3️⃣ Healenium – Self‑healing service (Docker‑Compose)

Create a `docker/healenium.yml` (or use the one that ships with the repo):

```yaml
# docker/healenium.yml
version: "3.8"
services:
  healenium:
    image: seleniumhq/healenium:latest
    ports:
      - "8080:8080"
    environment:
      - SELENIUM_HOST=selenium
      - SELENIUM_PORT=4444
    # Optional: mount a custom fallback‑map JSON
    # volumes:
    #   - ./fallback-map.json:/etc/healenium/fallback-map.json
```

Start the service:

```bash
docker-compose -f docker/healenium.yml up -d
# Verify it’s running:
curl http://localhost:8080/healthcheck   # should return {"status":"UP"}
```

## 4️⃣ Environment variables
Copy the example file and fill in your secrets:

```bash
cp .env.example .env
# Edit .env:
# APPLITOOLS_API_KEY=YOUR_EYES_KEY
# GEMINI_API_KEY=YOUR_GEMINI_KEY
# OPENAI_API_KEY=YOUR_OPENAI_KEY
```

## 5️⃣ Run the test suite locally
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

## 6️⃣ View Allure report locally
```bash
npm install -g allure-commandline   # if you don’t have it yet
allure serve allure-results
```

---

## 📂 Directory layout (relevant parts)

```
smart-qa-framework-python/
├── docs/
│   ├── setup.md          ← you are here
│   └── ai-modules.md
├── utils/
│   ├── api_client.py
│   ├── ai_data_generator.py
│   ├── visual_ai.py
│   └── self_healing.py
└── docker/
    └── healenium.yml