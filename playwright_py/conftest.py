# conftest.py — Playwright (Python) base fixtures for MarketMate
# This file defines shared pytest fixtures for Playwright tests:
# - creates a fresh browser context and page for each test
# - captures screenshots automatically on test failure
# - stores screenshots inside the test-results/ folder

from __future__ import annotations
import os
import pathlib
import pytest
from datetime import datetime
from dotenv import load_dotenv

# Load .env variables if present (optional, not required for tests)
load_dotenv()


@pytest.fixture(scope="session")
def artifacts_dir() -> pathlib.Path:
    """
    Create and return a folder for storing test artifacts
    (screenshots, traces, etc.). The folder is created once per session.
    """
    d = pathlib.Path("test-results")
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture()
def context(browser):
    """
    Create a new isolated Playwright browser context for each test.
    This acts like a clean incognito window — no shared cookies or cache.
    """
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 820},  # screen size for consistency
        accept_downloads=True,                    # allow file downloads
    )
    yield ctx
    ctx.close()  # always close context at the end of the test


@pytest.fixture()
def page(context, request, artifacts_dir):
    """
    Provide a new page (tab) from the browser context.
    If the test fails, automatically save a full-page screenshot
    to test-results/ with the test name and timestamp.
    """
    p = context.new_page()
    yield p

    # Check test outcome: 'failed' or 'passed' is stored by our hook below
    outcome = getattr(request.node, "_outcome", None)
    if outcome == "failed":
        # Build a timestamped, safe filename
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = request.node.nodeid.replace(os.sep, "_").replace("::", "__")
        png_path = artifacts_dir / f"{safe_name}__{ts}.png"

        # Try to capture a screenshot (ignore any internal Playwright errors)
        try:
            p.screenshot(path=str(png_path), full_page=True)
        except Exception:
            pass

    p.close()  # close the page regardless of pass/fail


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test call.
    It records whether the test passed or failed
    so the 'page' fixture knows when to save a screenshot.
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        setattr(item, "_outcome", "failed" if rep.failed else "passed")
