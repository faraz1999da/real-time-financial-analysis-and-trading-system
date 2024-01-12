import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer


@csrf_exempt
def ingest(request):
    if request.method == 'POST':
        data = request.body
        # Parse the incoming data as JSON
        data = json.loads(data)
        # Print the incoming data to the console
        # print(data)
        # Create a KafkaProducer object
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        # Send the data to the 'my-topic' Kafka topic
        producer.send('my-topic', json.dumps(data).encode('utf-8'))

        print("Data Sent was Successful!")
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


