import logging
import asyncio
import os
from .config import Config
from .kafka_client import KafkaClient
from .scraper import FacebookScraper
from .models import PostDTO
from .api import app
from .logging_config import setup_logging
from prometheus_client import start_http_server, Counter
from .metadata_scraper_adapter import scrape_facebook_page

setup_logging(Config.LOG_LEVEL)
logger = logging.getLogger("fbreaper.main")

# Prometheus metrics
SCRAPE_SUCCESS = Counter('scrape_success_total', 'Number of successful scrapes')
SCRAPE_FAILURE = Counter('scrape_failure_total', 'Number of failed scrapes')

shutdown_event = asyncio.Event()

async def process_command(command, kafka_client):
    if command.get("action") == "scrape":
        try:
            backend = Config.SCRAPER_BACKEND
            posts = []
            if backend == 'metadata':
                page_id = command.get("page_id") or command.get("url")
                posts = scrape_facebook_page(
                    page_id,
                    email=Config.SCRAPER_LOGIN_EMAIL,
                    password=Config.SCRAPER_LOGIN_PASSWORD,
                    max_posts=command.get("max_posts", 10)
                )
            else:
                async with FacebookScraper(
                    Config.SCRAPER_LOGIN_EMAIL,
                    Config.SCRAPER_LOGIN_PASSWORD,
                    Config.PLAYWRIGHT_HEADLESS
                ) as scraper:
                    posts = await scraper.scrape_posts(command["url"], command.get("max_posts", 10))
            for post in posts:
                kafka_client.produce_data(post.dict(), schema_name='PostDTO')
            logger.info(f"Scraped and published {len(posts)} posts.")
            SCRAPE_SUCCESS.inc()
        except Exception as e:
            logger.error(f"Scrape failed: {e}")
            SCRAPE_FAILURE.inc()

async def main():
    kafka_client = KafkaClient()
    for command in kafka_client.consume_commands():
        await process_command(command, kafka_client)

if __name__ == "__main__":
    import uvicorn
    from multiprocessing import Process

    def run_api():
        uvicorn.run("fbreaper_microservice.api:app", host="0.0.0.0", port=8000, log_level="info")

    api_proc = Process(target=run_api)
    api_proc.start()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        api_proc.terminate()
