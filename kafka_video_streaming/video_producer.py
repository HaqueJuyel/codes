from kafka import KafkaProducer
import cv2
import pickle
import time

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'vd-frames-topic'

# Load video file
cap = cv2.VideoCapture('song.mp4')  # Replace with your video file

frame_count = 0
print("Starting video stream to Kafka...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Serialize the frame using pickle
    data = pickle.dumps(frame)

    # Send frame to Kafka
    producer.send(topic, value=data)
    print(f"Sent frame {frame_count}")
    frame_count += 1

    # Simulate streaming (approx. 30 fps)
    time.sleep(0.03)

cap.release()
producer.flush()
print("Finished sending video frames.")
