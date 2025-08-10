import pytest
from fbreaper_microservice.kafka_client import KafkaClient
from unittest.mock import patch, MagicMock

def test_kafka_produce_and_consume(monkeypatch):
    # Mock KafkaProducer and KafkaConsumer
    with patch('fbreaper_microservice.kafka_client.KafkaProducer') as MockProducer, \
         patch('fbreaper_microservice.kafka_client.KafkaConsumer') as MockConsumer:
        mock_producer = MockProducer.return_value
        mock_consumer = MockConsumer.return_value
        mock_consumer.__iter__.return_value = [MagicMock(value={"action": "scrape", "url": "test"})]
        client = KafkaClient()
        client.produce_data({"id": "1", "author": "a", "content": "c", "timestamp": "t", "hashtags": [], "language": "en"}, schema_name='PostDTO')
        commands = list(client.consume_commands())
        assert commands[0]["action"] == "scrape"
