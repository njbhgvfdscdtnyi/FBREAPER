import json
from kafka import KafkaConsumer
from neo4j import GraphDatabase

# Kafka config
consumer = KafkaConsumer(
    'nlp-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Neo4j config
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def store_post(tx, post_id, text, language, sentiment, hashtags, entities):
    tx.run("""
        MERGE (p:Post {id: $post_id})
        SET p.text = $text, p.language = $language, p.sentiment = $sentiment
    """, post_id=post_id, text=text, language=language, sentiment=sentiment)

    for tag in hashtags:
        tx.run("""
            MERGE (h:Hashtag {name: $tag})
            MERGE (p:Post {id: $post_id})-[:HAS_HASHTAG]->(h)
        """, tag=tag, post_id=post_id)

    for ent in entities:
        tx.run("""
            MERGE (e:Entity {name: $ent})
            MERGE (p:Post {id: $post_id})-[:MENTIONS]->(e)
        """, ent=ent, post_id=post_id)

print("Link Analysis Service started, listening for NLP data...")
with driver.session() as session:
    for msg in consumer:
        data = msg.value
        post_id = data.get("id", None)
        text = data.get("original_text", "")
        language = data.get("language", "unknown")
        sentiment = data.get("sentiment", 0)
        hashtags = data.get("hashtags", [])
        entities = data.get("entities", [])

        if post_id:
            session.write_transaction(
                store_post, post_id, text, language, sentiment, hashtags, entities
            )
            print(f"Stored post {post_id} with hashtags {hashtags} and entities {entities}")
