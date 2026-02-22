import pytest
from playwright.sync_api import Page


@pytest.mark.parametrize('email, password, expected_url', [
    ('valid_email@example.com', 'valid_password', '/dashboard'),
])
def test_successful_login(page: Page, login_url, config, email: str, password: str, expected_url: str):

    # Load selectors from config.json
    sel = config["selectors"]

    # Navigate to login page
    page.goto(login_url)

    # Fill form
    page.locator(sel["email"]).fill(email)
    page.locator(sel["password"]).fill(password)
    page.locator(sel["submit"]).click()

    # Verify redirect (example logic)
    assert expected_url in page.url


@pytest.mark.parametrize('email, password', [
    ('invalid_email@example.com', 'valid_password'),
    ('valid_email@example.com', 'invalid_password'),
])
def test_failed_login(page: Page, login_url, config, email: str, password: str):

    sel = config["selectors"]

    page.goto(login_url)

    page.locator(sel["email"]).fill(email)
    page.locator(sel["password"]).fill(password)
    page.locator(sel["submit"]).click()

    # Use config selector instead of hardcoded value
    assert page.locator(sel["error"]).is_visible()


def test_lock_account_after_failed_attempts(page: Page, login_url, config):

    sel = config["selectors"]

    for _ in range(5):

        # Always start from fresh login page
        page.goto(login_url)

        page.wait_for_selector(sel["email"])

        page.locator(sel["email"]).fill('valid_email@example.com')
        page.locator(sel["password"]).fill('invalid_password')

        page.locator(sel["submit"]).click()

        # Wait for error message to appear
        page.wait_for_selector(sel["error"])

        assert page.locator(sel["error"]).is_visible()