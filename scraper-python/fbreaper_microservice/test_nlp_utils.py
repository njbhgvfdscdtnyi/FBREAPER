from fbreaper_microservice import nlp_utils

def test_detect_language():
    assert nlp_utils.detect_language("Hello world") in ["en", "unknown"]

def test_translate_text():
    # Should return original if LibreTranslate is not running
    assert nlp_utils.translate_text("Hello", "es") in ["Hello", "Hola"]

def test_sentiment_analysis():
    assert nlp_utils.sentiment_analysis("I love this!") == "positive"
    assert nlp_utils.sentiment_analysis("I hate this!") == "negative"
    assert nlp_utils.sentiment_analysis("") == "neutral"

def test_extract_hashtags():
    assert nlp_utils.extract_hashtags("#hello #world") == ["hello", "world"]
