import json
import re
from kafka import KafkaConsumer, KafkaProducer
from textblob import TextBlob
import requests
from neo4j import GraphDatabase

KAFKA_BROKER = "localhost:9092"
SCRAPER_TOPIC = "scraper-data"
NLP_TOPIC = "nlp-data"
LIBRETRANSLATE_URL = "http://localhost:5000/translate"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

consumer = KafkaConsumer(
    SCRAPER_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

def extract_hashtags(text):
    return re.findall(r"#(\w+)", text)

def detect_language(text):
    try:
        return TextBlob(text).detect_language()
    except:
        return "unknown"

def translate_text(text, target_lang="en"):
    try:
        response = requests.post(LIBRETRANSLATE_URL, json={
            "q": text,
            "source": "auto",
            "target": target_lang,
            "format": "text"
        })
        return response.json().get("translatedText", text)
    except:
        return text

def store_in_neo4j(post_data):
    with neo4j_driver.session() as session:
        session.run("""
            MERGE (p:Post {content: $content})
            SET p.sentiment = $sentiment,
                p.language = $language,
                p.translation = $translation
        """, **post_data)

print("[NLP] Service started. Listening for messages...")

for message in consumer:
    post = message.value
    text = post.get("content", "")

    hashtags = extract_hashtags(text)
    sentiment = TextBlob(text).sentiment.polarity
    language = detect_language(text)
    translation = translate_text(text) if language != "en" else text

    processed = {
        "content": text,
        "hashtags": hashtags,
        "sentiment": sentiment,
        "language": language,
        "translation": translation
    }

    producer.send(NLP_TOPIC, processed)
    store_in_neo4j(processed)
    print(f"[NLP] Processed and sent: {processed}")
