import requests
import re
from textblob import TextBlob
from .config import Config
import logging

logger = logging.getLogger("fbreaper.nlp")

def detect_language(text: str) -> str:
    try:
        blob = TextBlob(text)
        return blob.detect_language()
    except Exception:
        return 'unknown'
    try:
        blob = TextBlob(text)
        return blob.detect_language()
    except Exception as e:
        logger.warning(f"Language detection failed: {e}")
        return 'unknown'

def translate_text(text: str, target_lang: str = 'en') -> str:
    try:
        resp = requests.post(Config.LIBRETRANSLATE_URL, data={
            'q': text,
            'source': 'auto',
            'target': target_lang
        })
        if resp.ok:
            return resp.json().get('translatedText', text)
        logger.warning(f"LibreTranslate error: {resp.text}")
    except Exception:
        pass
    except requests.Timeout:
        logger.error("LibreTranslate request timed out.")
    except Exception as e:
        logger.error(f"LibreTranslate failed: {e}")
    return text

def sentiment_analysis(text: str) -> str:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    return 'neutral'
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        return 'neutral'
    except Exception as e:
        logger.warning(f"Sentiment analysis failed: {e}")
        return 'neutral'

def extract_hashtags(text: str):
    return re.findall(r"#(\w+)", text)
    return re.findall(r"#(\w+)", text)
