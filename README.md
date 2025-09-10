1  # MarketMate Test Automation
2
3  ## Run locally
4  python -m venv .venv
5  # Linux/macOS
6  source .venv/bin/activate
7  # Windows (PowerShell)
8  # .venv\Scripts\Activate.ps1
9
10 pip install -r requirements.txt
11
12 # Run all tests
13 pytest
14
15 ## Structure
16 - pages/: Page Objects
17 - tests/: Test suites (pytest)
18 - utils/: Shared helpers
