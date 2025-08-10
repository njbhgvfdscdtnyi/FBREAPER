import pytest
from unittest.mock import patch, AsyncMock
from fbreaper_microservice.scraper import FacebookScraper

@pytest.mark.asyncio
async def test_scraper_login_and_scrape(monkeypatch):
    # Patch Playwright and FacebookScraper internals
    with patch('fbreaper_microservice.scraper.async_playwright') as mock_playwright:
        mock_pw = mock_playwright.return_value.__aenter__.return_value
        mock_browser = AsyncMock()
        mock_context = AsyncMock()
        mock_page = AsyncMock()
        mock_pw.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.goto.return_value = None
        mock_page.wait_for_load_state.return_value = None
        mock_page.query_selector.return_value = True
        mock_page.query_selector_all.return_value = []
        scraper = FacebookScraper('email', 'pass', headless=True)
        async with scraper:
            posts = await scraper.scrape_posts('http://test', max_posts=1)
            assert isinstance(posts, list)
