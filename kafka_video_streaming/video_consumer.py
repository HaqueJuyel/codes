from kafka import KafkaConsumer
import cv2
import pickle

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'vd-frames-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='video-stream-player'
)

print("Receiving and playing video stream...")

for message in consumer:
    # Deserialize frame
    frame = pickle.loads(message.value)

    # Display the frame
    cv2.imshow('Kafka Video Stream', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print("Stream closed.")
