import asyncio
import logging
from playwright.async_api import async_playwright
from .nlp_utils import detect_language, translate_text, sentiment_analysis, extract_hashtags
from .models import PostDTO, CommentDTO

logger = logging.getLogger("fbreaper.scraper")

class FacebookScraper:
    def __init__(self, email, password, headless=True):
        self.email = email
        self.password = password
        self.headless = headless
        self.context = None
        self.page = None
        self.browser = None

    async def __aenter__(self):
        from playwright.async_api import async_playwright
        self._playwright = await async_playwright().start()
        await self.login()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
        await self._playwright.stop()

    async def login(self):
        self.browser = await self._playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        await self.page.goto("https://www.facebook.com/login")
        await self.page.fill('input[name="email"]', self.email)
        await self.page.fill('input[name="pass"]', self.password)
        await self.page.click('button[name="login"]')
        await self.page.wait_for_load_state('networkidle')
        logger.info("Logged in to Facebook.")

    async def scrape_posts(self, url, max_posts=10):
        posts = []
        await self.page.goto(url)
        await self.page.wait_for_load_state('networkidle')
        for _ in range(max_posts):
            await self.page.mouse.wheel(0, 1000)
            await asyncio.sleep(1)
        post_elements = await self.page.query_selector_all('div[data-ad-preview="message"]')
        for idx, el in enumerate(post_elements[:max_posts]):
            content = await el.inner_text()
            author = "Unknown"
            timestamp = "Unknown"
            lang = detect_language(content)
            translated = translate_text(content, 'en') if lang != 'en' else content
            sentiment = sentiment_analysis(translated)
            hashtags = extract_hashtags(content)
            post = PostDTO(
                id=f"post_{idx}",
                author=author,
                content=content,
                timestamp=timestamp,
                hashtags=hashtags,
                language=lang,
                sentiment=sentiment
            )
            posts.append(post)
        return posts

    async def close(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
