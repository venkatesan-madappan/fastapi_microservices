from kafka import KafkaConsumer

consumer = KafkaConsumer('test-topic', 
                         bootstrap_servers='localhost:9092', 
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='my-group',
)

print("Listening for messages on topic: test-topic")

for message in consumer:
    print(f"Received : {message.value.decode('utf-8')}")

