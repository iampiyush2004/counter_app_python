


from flask import Flask, request
from flask_socketio import SocketIO
from num2words import num2words
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

clients = {}  # Stores { 'client1': sid, 'client2': sid }
last_numbers = {'client1': 1, 'client2': 2}  # Tracks last number for each client

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/health")
def health():
    return "OK", 200


@socketio.on('connect')
def handle_connect():
    global clients

    # Assign client to an available slot (client1 or client2)
    if 'client1' not in clients:
        client_id = 'client1'
    elif 'client2' not in clients:
        client_id = 'client2'
    else:
        print("More than 2 clients attempted to connect, rejecting connection.")
        return  # No more than 2 clients allowed

    clients[client_id] = request.sid
    print(f"Client {client_id} connected and assigned.")

    # Send assignment and last number info
    socketio.emit('client_assigned', {'client_id': client_id, 'last_number': last_numbers[client_id]}, room=request.sid)

    # Start the game if 2 clients are connected
    if len(clients) == 2:
        socketio.emit('start_game')

@socketio.on('disconnect')
def handle_disconnect():
    global clients

    disconnected_client = None
    for client_id, sid in list(clients.items()):
        if sid == request.sid:
            disconnected_client = client_id
            del clients[client_id]
            print(f"Client {client_id} disconnected.")

    # Stop game only if one client remains
    if len(clients) < 2:
        print("Waiting for another client to connect...")
        socketio.emit('stop_game')

@socketio.on('number')
def handle_number(data):
    global last_numbers

    client_id = data['client_id']
    number = data['number']

    # Update the last counted number for that client
    last_numbers[client_id] = number + 2

    word = num2words(number)
    with open(os.path.join(DATA_DIR, "numbers.txt"), "a") as f:
        f.write(f"{word}\n")

    print(f"Received {word} from {client_id}")

if __name__ == "__main__":
    print("Server starting...")
    socketio.run(app, host="0.0.0.0", port=5000)
