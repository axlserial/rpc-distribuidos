import socket
from xmlrpc.server import SimpleXMLRPCServer


def get_ip_address():
    """Obtiene la dirección IP de la máquina"""
    # return "192.168.195.179"

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


players = 0
player_one_choice = None
player_two_choice = None

player_one_reset = False
player_two_reset = False


# Cuando un cliente se conecta, se le asigna un número de jugador
def connection():
    global players
    players += 1

    print(f"Client {players} connected")

    return players


# Cuando un cliente envía su elección, se guarda en una variable global
def send_choice(player, choice):
    global player_one_choice, player_two_choice
    print("Choice received")

    if player == 1:
        player_one_choice = choice
    else:
        player_two_choice = choice

    return choice


# Para reseteo de jugadas
def reset_play(player):
    global player_one_choice, player_two_choice
    global player_one_reset, player_two_reset

    if player == 1:
        player_one_reset = True
    else:
        player_two_reset = True

    if player_one_reset and player_two_reset:
        player_one_choice = None
        player_two_choice = None

        # Sí ambos jugadores resetearon
        return "reset"

    # Sí solo un jugador reseteó
    return "waiting"


# Definir la lógica del juego
def make_play():
    global player_one_choice, player_two_choice
    valid_choices = ["piedra", "papel", "tijeras"]

    if player_one_choice is None or player_two_choice is None:
        return "waiting"

    if (
        player_one_choice not in valid_choices
        or player_two_choice not in valid_choices
    ):
        return (
            "Jugada inválida. Las opciones válidas son: piedra, papel, tijeras."
        )

    if player_one_choice == player_two_choice:
        result = "Empate"
    elif (
        (player_one_choice == "piedra" and player_two_choice == "tijeras")
        or (player_one_choice == "papel" and player_two_choice == "piedra")
        or (player_one_choice == "tijeras" and player_two_choice == "papel")
    ):
        result = "Jugador 1 gana"
    else:
        result = "Jugador 2 gana"

    return result


# Crear el servidor RPC
server = SimpleXMLRPCServer((get_ip_address(), 8000))
print(f"Server running on {get_ip_address()}:8000")

# Registrar las funciones RPC del juego
server.register_function(connection, "connection")
server.register_function(send_choice, "send_choice")
server.register_function(make_play, "make_play")
server.register_function(reset_play, "reset_play")

# Servidor
server.serve_forever()
