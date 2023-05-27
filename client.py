from xmlrpc.client import ServerProxy
from threading import Thread

# Conectar al servidor RPC
server = ServerProxy("http://localhost:8000/")

# Obtener el número de player
player = server.connection()

def play():
    global server, player
    choice = input("Elige piedra, papel o tijeras: ")
    server.send_choice(player, choice)

    result = server.make_play()
    while result == "waiting":
        result = server.make_play()

    print(result)

# Hilo
thread = Thread(target=play)
thread.start()
thread.join()