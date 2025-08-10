import logging
from MetaDataScraper import LoginlessScraper, LoggedInScraper
from .models import PostDTO
from .config import Config

logger = logging.getLogger("fbreaper.metadata_scraper_adapter")

def scrape_facebook_page(page_id, email=None, password=None, max_posts=10):
    """
    Uses MetaDataScraper to fetch Facebook page data.
    If email/password provided, uses logged-in scraping for more access.
    Returns: list of PostDTO
    """
    try:
        if email and password:
            scraper = LoggedInScraper(page_id, email, password)
        else:
            scraper = LoginlessScraper(page_id)
        result = scraper.scrape()
        posts = []
        post_texts = result.get('post_texts', [])
        for idx, text in enumerate(post_texts[:max_posts]):
            post = PostDTO(
                id=f"post_{idx}",
                author=result.get('page_name', 'Unknown'),
                content=text,
                timestamp="Unknown",  # MetaDataScraper may not provide timestamp
                hashtags=[],  # Can extract with NLP utils if needed
                language="unknown",
                sentiment=None
            )
            posts.append(post)
        return posts
    except Exception as e:
        logger.error(f"MetaDataScraper error: {e}")
        return []
