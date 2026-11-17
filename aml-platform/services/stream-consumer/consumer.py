"""Kafka boundary consumer. Starts after API/database are configured."""
import json
from kafka import KafkaConsumer
from app_placeholder import process  # Replace with an authenticated API call or shared service package.
consumer=KafkaConsumer("transactions.raw",bootstrap_servers=["localhost:9092"],
    value_deserializer=lambda b:json.loads(b.decode()),group_id="aml-monitoring")
for message in consumer:
    process(message.value)
