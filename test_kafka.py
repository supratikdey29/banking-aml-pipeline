from confluent_kafka import Producer
from dotenv import load_dotenv
import os

load_dotenv()

conf = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'security.protocol': os.getenv('SECURITY_PROTOCOL'),
    'sasl.mechanisms': os.getenv('SASL_MECHANISM'),
    'sasl.username': os.getenv('KAFKA_API_KEY'),
    'sasl.password': os.getenv('KAFKA_API_SECRET')
}

producer = Producer(conf)

print("Kafka connection successful")