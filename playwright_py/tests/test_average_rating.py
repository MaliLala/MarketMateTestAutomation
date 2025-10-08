import re
import pytest
from pages.shop_page import ShopPage
from pages.product_page import ProductPage

pytestmark = pytest.mark.smoke

def test_average_rating(page):
    """
    GIVEN the Store
    WHEN the first product is opened
    THEN an average rating (if present) is readable and sane (0..5)
    """
    shop = ShopPage(page).open()
    product = shop.open_first_product()
    assert isinstance(product, ProductPage) and product.is_displayed(), "Failed to open a product page"

    # Try common rating patterns: "4.2", "4 out of 5", star aria-labels, etc.
    # Keep it simple and tolerant.
    locs = [
        page.locator("text=/out of 5/i").first,
        page.get_by_role("img", name=re.compile(r"out of 5", re.I)).first,
        page.locator("text=/rating|reviews?/i").first,
    ]

    text = ""
    for l in locs:
        if l.count() > 0 and l.is_visible():
            t = l.text_content() or l.get_attribute("aria-label") or l.get_attribute("title") or ""
            text = (t or "").strip()
            if text:
                break

    if not text:
        pytest.skip("No rating UI present on this product page")

    m = re.search(r"(\d+(?:[.,]\d+)?)", text)
    assert m, f"Could not parse rating from: {text!r}"
    val = float(m.group(1).replace(",", "."))
    assert 0.0 <= val <= 5.0, f"Rating {val} not in expected range 0..5"
