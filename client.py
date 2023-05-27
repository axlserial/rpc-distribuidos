from xmlrpc.client import ServerProxy
from threading import Thread

# Conectar al servidor RPC
server = ServerProxy("http://192.168.1.64:8000/")

# Obtener el número de player
player = server.connection()


def play():
    while True:
        global server, player
        server.reset_choice(player)
        choice = input("Choose rock, paper or scissors: ")
        server.send_choice(player, choice)

        result = server.get_result(player)
        while result == "waiting":
            result = server.get_result(player)

        print(result)

        wants_to_play = input("Do you want to play again? (y/n): ")
        if wants_to_play == "n":
            server.disconnect(player)
            break


# Hilo
thread = Thread(target=play)
thread.start()
thread.join()
