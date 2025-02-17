# import socketio
# import time
# from num2words import num2words
# import os

# class CountingClient:
#     def __init__(self):
#         self.sio = socketio.Client()
#         self.client_id = None
#         self.is_counting = False
#         self.setup_handlers()

#     def setup_handlers(self):
#         @self.sio.on('connect')
#         def on_connect():
#             print("Connected to server!")

#         @self.sio.on('disconnect')
#         def on_disconnect():
#             print("Disconnected from server!")
#             self.is_counting = False

#         @self.sio.on('client_assigned')
#         def on_client_assigned(data):
#             self.client_id = data['client_id']
#             print(f"Assigned as {self.client_id}")

#         @self.sio.on('start_game')
#         def on_start_game():
#             print("Game starting!")
#             self.is_counting = True

#         @self.sio.on('stop_game')
#         def on_stop_game():
#             print("Game stopped!")
#             self.is_counting = False

#     def should_count(self, number):
#         if self.client_id == 'client1':
#             return number % 2 == 1  # Client 1 counts odd numbers
#         elif self.client_id == 'client2':
#             return number % 2 == 0  # Client 2 counts even numbers
#         return False  # Default case (should not happen)

#     def run(self):
#         SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:5000')
        
#         try:
#             self.sio.connect(SERVER_URL)
#             number = 1
            
#             while True:
#                 if self.is_counting and self.client_id:
#                     if self.should_count(number):
#                         word = num2words(number)
#                         print(f"{self.client_id} counting: {word}")
#                         self.sio.emit('number', {'number': number})
#                         time.sleep(1)  # Wait 1 second before next number
                    
#                     if number >= 500:  # Stop at 500
#                         break
                        
#                     number += 1
#                 time.sleep(0.1)  # Small delay when not counting

#         except Exception as e:
#             print(f"Error: {e}")
#         finally:
#             if self.sio.connected:
#                 self.sio.disconnect()

# if __name__ == "__main__":
#     client = CountingClient()
#     client.run()


import socketio
import time
from num2words import num2words
import os

class CountingClient:
    def __init__(self):
        self.sio = socketio.Client()
        self.client_id = None
        self.last_number = None  # Store the last counted number
        self.is_counting = False
        self.setup_handlers()

    def setup_handlers(self):
        @self.sio.on('connect')
        def on_connect():
            print("Connected to server!")

        @self.sio.on('disconnect')
        def on_disconnect():
            print("Disconnected from server!")
            self.is_counting = False

        @self.sio.on('client_assigned')
        def on_client_assigned(data):
            self.client_id = data['client_id']
            self.last_number = data['last_number']  # Get last number from server
            print(f"Assigned as {self.client_id}, resuming from {self.last_number}")

        @self.sio.on('start_game')
        def on_start_game():
            print("Game starting!")
            self.is_counting = True

        @self.sio.on('stop_game')
        def on_stop_game():
            print("Game stopped!")
            self.is_counting = False

    def should_count(self, number):
        if self.client_id == 'client1':
            return number % 2 == 1  # Client 1 counts odd numbers
        elif self.client_id == 'client2':
            return number % 2 == 0  # Client 2 counts even numbers
        return False

    def run(self):
        SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:5000')

        try:
            self.sio.connect(SERVER_URL)

            # Start from last counted number or initial value
            number = self.last_number if self.last_number else (1 if self.client_id == 'client1' else 2)

            while True:
                if self.is_counting and self.client_id:
                    if self.should_count(number):
                        word = num2words(number)
                        print(f"{self.client_id} counting: {word}")
                        self.sio.emit('number', {'client_id': self.client_id, 'number': number})
                        time.sleep(1)  # Wait 1 second
                    
                    if number >= 2000:  # Stop at 2000
                        break

                    number += 1
                time.sleep(0.1)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if self.sio.connected:
                self.sio.disconnect()

if __name__ == "__main__":
    client = CountingClient()
    client.run()
