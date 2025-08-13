from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092")

topic = "test-topic"

message = "Hello Friend! Im Python Kafka Producer"

for i in range(10):
    producer.send(topic, value=message.encode('utf-8'))
    producer.flush()
    message = input("> ")

