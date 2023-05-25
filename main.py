# Servidor.py
from xmlrpc.server import SimpleXMLRPCServer
import threading


class OptionsHandler:
    def __init__(self):
        self.client_one_answer = None
        self.client_two_answer = None
        self.clients_connected = 0
        self.clients_choices = []
        self.event = threading.Event()

    def connect(self):
        self.clients_connected += 1
        print(f'Client {self.clients_connected} connected')
        return 1

    def send_choice(self):
        print('Choice received')
        self.clients_choices.append(1)
        return 1

    def send_response(self):
        self.event.set()

    def get_response(self):
        self.event.wait()
        #return self.client_one_answer, self.client_two_answer
        self.event.clear()
        return 'yastan los dos'

server = SimpleXMLRPCServer(("localhost", 5000))
print('Server running on port 5000')

options_handler = OptionsHandler()

server.register_function(options_handler.connect, "connect")
server.register_function(options_handler.send_choice, "send_choice")
server.register_function(options_handler.get_response, "get_response")

# def send_messages_async():
#     while True:
#         while len(options_handler.clients_choices) < 2:
#             pass

#         print('Sending messages')
#         options_handler.send_response()

# thread = threading.Thread(target=send_messages_async)
# thread.start()

server.serve_forever()
