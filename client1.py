import time
import socketio
from num2words import num2words

sio = socketio.Client()

sio.connect("http://localhost:5000")

number = 1  # Start with the first odd number

while number <= 500:
    word = num2words(number)  # Convert number to words
    print(f"Client 1 sending: {word}")
    sio.send(word)  # Send to server
    time.sleep(1)  # Wait 1 second
    number += 2  # Move to the next odd number
