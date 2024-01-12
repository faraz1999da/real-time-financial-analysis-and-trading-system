# This is for testing purposes

import numpy as np
import json
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer('my-signal-topic', bootstrap_servers=['localhost:9092'])

for message in consumer:
    data = json.loads(message.value)
    print(data)

