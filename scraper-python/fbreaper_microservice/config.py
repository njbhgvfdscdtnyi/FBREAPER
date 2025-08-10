import os

class Config:
    KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
    KAFKA_SCRAPER_CONTROL_TOPIC = os.getenv('KAFKA_SCRAPER_CONTROL_TOPIC', 'scraper-control')
    KAFKA_OUTPUT_TOPIC = os.getenv('KAFKA_OUTPUT_TOPIC', 'fbreaper-topic')
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
    LIBRETRANSLATE_URL = os.getenv('LIBRETRANSLATE_URL', 'http://localhost:5000/translate')
    SCRAPER_LOGIN_EMAIL = os.getenv('SCRAPER_LOGIN_EMAIL', '')
    SCRAPER_LOGIN_PASSWORD = os.getenv('SCRAPER_LOGIN_PASSWORD', '')
    PLAYWRIGHT_HEADLESS = os.getenv('PLAYWRIGHT_HEADLESS', 'true').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    SCRAPER_BACKEND = os.getenv('SCRAPER_BACKEND', 'playwright')  # 'playwright' or 'metadata'
