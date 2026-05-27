import json
from kafka import KafkaProducer
from datetime import datetime, date


# =====================================================
# JSON SERIALIZER (IMPORTANT FIX)
# =====================================================
def json_serializer(obj):

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    return str(obj)


class KafkaProducerClient:

    def __init__(self):

        self.producer = KafkaProducer(

            bootstrap_servers="pkc-921jm.us-east-2.aws.confluent.cloud:9092",

            security_protocol="SASL_SSL",

            sasl_mechanism="PLAIN",

            sasl_plain_username="WUCCZM2M6V6XETNB",

            sasl_plain_password="cfltDUbf0P5DTjH/Jhv6MmXQgsK48xXDArdF91LlbRsQmChs5WZBR2R526yGS8aQ",

            value_serializer=lambda v: json.dumps(v, default=json_serializer).encode("utf-8"),

            key_serializer=lambda k: str(k).encode("utf-8")
        )

    def send(self, topic, key, value):

        self.producer.send(topic, key=key, value=value)

    def flush(self):

        self.producer.flush()