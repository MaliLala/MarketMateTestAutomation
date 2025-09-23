

cd ~/Portfolio-projects/MarketMateTestAutomation

cat > README.md << 'EOF'
# MarketMate Test Automation

Automated end-to-end test suite for the MarketMate webshop (Selenium + pytest).  
This repository contains page objects, Selenium flows and supporting QA documentation.

Quickstart
1. Create and activate a Python virtual environment:
   python -m venv .venv
   # macOS / Linux
   source .venv/bin/activate
   # Windows (PowerShell)
   # .venv\Scripts\Activate.ps1

2. Install dependencies:
   pip install -r requirements.txt

3. Run the test suite:
   pytest

Project structure
- pages/ — Page Objects (encapsulate UI interactions)
- tests/ — Pytest test modules (Selenium flows and unit checks)
- utils/ — Helpers and utilities used across tests
- docs/ — Test plan, environment setup and other QA docs

Playwright notes (planned)
- Playwright Python and Playwright TypeScript suites will live in separate folders (e.g. playwright-python/ and playwright-ts/) to avoid mixing runtimes.

Contact
- GitHub: https://github.com/MaliLala
- LinkedIn: https://www.linkedin.com/in/goran-csonkity
EOF
