import time
import socketio
from num2words import num2words

sio = socketio.Client()

sio.connect("http://localhost:5000")

number = 2  # Start with the first even number

while number <= 500:
    word = num2words(number)  # Convert number to words
    print(f"Client 2 sending: {word}")
    sio.send(word)  # Send to server
    time.sleep(1)  # Wait 1 second
    number += 2  # Move to the next even number
