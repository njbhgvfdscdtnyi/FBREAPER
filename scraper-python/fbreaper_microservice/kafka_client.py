import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from .config import Config

logger = logging.getLogger("fbreaper.kafka")

class KafkaClient:
    def __init__(self):
        self.consumer = KafkaConsumer(
            Config.KAFKA_SCRAPER_CONTROL_TOPIC,
            bootstrap_servers=Config.KAFKA_BROKER,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='fbreaper-scraper-group',
        )
        self.producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def consume_commands(self):
        for message in self.consumer:
            logger.info(f"Received command: {message.value}")
            yield message.value

    def produce_data(self, data, topic=None):
        topic = topic or Config.KAFKA_OUTPUT_TOPIC
        self.producer.send(topic, data)
        self.producer.flush()
        logger.info(f"Produced data to {topic}")
