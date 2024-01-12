from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from kafka import KafkaConsumer
import time


def display(request):
    # # Connect to the Kafka topic
    consumer = KafkaConsumer('my-signal-topic', bootstrap_servers=['localhost:9092'])
    # # Read the messages from the Kafka topic
    # messages = []
    message = next(consumer, None)
    print(message)

    if message:
        # Simulate a delay of 2 seconds (adjust as needed)
        time.sleep(2)
        message_value = message.value.decode('utf-8')
        return JsonResponse({'message': message_value})
    else:
        return JsonResponse({'message': None})