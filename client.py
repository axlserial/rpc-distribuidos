import xmlrpc.client
import threading

client = xmlrpc.client.ServerProxy("http://localhost:5000/")

client.connect()
client.send_choice()
def get_response():
	result = client.get_response()
	print(result)

thread = threading.Thread(target=get_response)
thread.start()

while True:
    pass