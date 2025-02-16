# import time
# import socketio
# from num2words import num2words
# import os

# sio = socketio.Client()

# # Get server URL from environment variable, default to localhost for local development
# SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:5000')
# print(f"Attempting to connect to server at {SERVER_URL}")

# try:
#     sio.connect(SERVER_URL)
#     print("Successfully connected to server!")

#     number = 2  # Start with the first even number
#     while number <= 500:
#         word = num2words(number)  # Convert number to words
#         print(f"Client 2 sending: {word}")
#         sio.send(word)  # Send to server
#         time.sleep(1)  # Wait 1 second
#         number += 2  # Move to the next even number

# except Exception as e:
#     print(f"Error connecting to server: {e}")
#     raise


import time
import socketio
from num2words import num2words
import os

sio = socketio.Client()

# Get server URL from environment variable, default to localhost for local development
SERVER_URL = os.getenv('SERVER_URL', 'http://server:5000')
print(f"Attempting to connect to server at {SERVER_URL}")

try:
    sio.connect(SERVER_URL)
    print("Successfully connected to server!")

    number = 2  # Start with the first even number
    while number <= 500:
        word = num2words(number)  # Convert number to words
        print(f"Client 2 sending: {word}")
        sio.send(word)  # Send to server
        time.sleep(1)  # Wait 1 second
        number += 2  # Move to the next even number

except Exception as e:
    print(f"Error connecting to server: {e}")
    raise
