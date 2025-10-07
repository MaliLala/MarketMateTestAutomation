import pytest

# Mark this file as a smoke test
pytestmark = pytest.mark.smoke

# Public home page of the MarketMate app
HOME_URL = "https://grocerymate.masterschool.com/"

def test_homepage_loads(page):
    """
    GIVEN the user opens the GroceryMate homepage
    WHEN the page is loaded
    THEN the response should be successful and basic UI elements should exist
    """
    # Navigate to the home page and wait for the DOM to load
    resp = page.goto(HOME_URL, wait_until="domcontentloaded")

    # Verify navigation succeeded and returned a valid HTTP 2xx response
    assert resp is not None and resp.ok, f"Navigation failed: {resp.status if resp else 'no response'}"

    # Check that the page title contains expected words (loose match)
    title = page.title()
    assert isinstance(title, str) and len(title) > 0
    assert any(keyword in title.lower() for keyword in ["grocery", "market", "mate"])

    # Look for at least one <h1> heading element (accessibility check)
    h1_count = page.get_by_role("heading", level=1).count()
    assert h1_count > 0, "No main heading (H1) found on the homepage"
