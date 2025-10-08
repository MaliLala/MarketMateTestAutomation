import pytest
from pages.shop_page import ShopPage

pytestmark = pytest.mark.smoke

def test_age_verification(page):
    """
    GIVEN the Store page with DOB gate
    WHEN a valid DOB is entered and confirmed
    THEN product actions are visible (e.g., an Add to Cart button)
    """
    shop = ShopPage(page).open()      # opens /store and best-effort passes DOB
    # After the helper, we still assert something product-like is visible
    assert page.locator("button.btn-cart").first.count() > 0, "No 'Add to Cart' found after age verification"
