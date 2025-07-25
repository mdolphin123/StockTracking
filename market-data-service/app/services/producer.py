import time
import json
from datetime import datetime
from kafka import KafkaProducer


def serializer(message):
    return json.dumps(message).encode("utf-8")

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    api_version=(0,11,5),
    value_serializer=serializer,
)
