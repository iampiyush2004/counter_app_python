# from flask import Flask
# from flask_socketio import SocketIO
# from num2words import num2words

# app = Flask(__name__)
# socketio = SocketIO(app, async_mode="eventlet")

# expected_number = 1  # Start from 1

# @socketio.on("message")
# def handle_message(msg):
#     global expected_number

#     expected_word = num2words(expected_number)  # Convert expected number to words

#     if msg.strip().lower() == expected_word:
#         print(f"✅ Received: {msg}")

#         # Write the valid number spelling to the file
#         with open("numbers.txt", "a") as f:
#             f.write(msg + "\n")

#         expected_number += 1  # Move to the next number
#     else:
#         print(f"❌ Unexpected message: {msg}, expected: {expected_word}")

# if __name__ == "__main__":
#     socketio.run(app, host="0.0.0.0", port=5000)



from flask import Flask
from flask_socketio import SocketIO
from num2words import num2words
import os

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

expected_number = 1  # Start from 1
DATA_DIR = "/app/data"  # Directory for data in container

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/health')
def health_check():
    return 'OK', 200

@socketio.on("message")
def handle_message(msg):
    global expected_number

    expected_word = num2words(expected_number)  # Convert expected number to words

    if msg.strip().lower() == expected_word:
        print(f"✅ Received: {msg}")

        # Write the valid number spelling to the file
        with open(os.path.join(DATA_DIR, "numbers.txt"), "a") as f:
            f.write(msg + "\n")

        expected_number += 1  # Move to the next number
    else:
        print(f"❌ Unexpected message: {msg}, expected: {expected_word}")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)