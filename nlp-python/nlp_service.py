import json
from kafka import KafkaConsumer, KafkaProducer
from textblob import TextBlob
import re
import requests

# Kafka setup
consumer = KafkaConsumer(
    'scraper-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

# LibreTranslate API endpoint
TRANSLATE_URL = "http://localhost:5000/translate"

def detect_language(text):
    try:
        blob = TextBlob(text)
        return blob.detect_language()
    except Exception:
        return "unknown"

def translate_text(text, target_lang="en"):
    try:
        resp = requests.post(TRANSLATE_URL, data={
            'q': text,
            'source': 'auto',
            'target': target_lang,
            'format': 'text'
        })
        return resp.json().get("translatedText", text)
    except:
        return text

def extract_hashtags(text):
    return re.findall(r"#(\w+)", text)

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def entity_linking(text):
    # Placeholder for entity linking logic
    return []

print("NLP Service started, waiting for messages...")
for msg in consumer:
    data = msg.value
    text_content = data.get("text", "")

    result = {
        "original_text": text_content,
        "language": detect_language(text_content),
        "translated_text": translate_text(text_content),
        "hashtags": extract_hashtags(text_content),
        "sentiment": analyze_sentiment(text_content),
        "entities": entity_linking(text_content)
    }

    producer.send("nlp-data", result)
    print("Processed:", result)
