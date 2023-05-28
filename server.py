import socket
from xmlrpc.server import SimpleXMLRPCServer


def get_ip_address():
    """Obtiene la dirección IP de la máquina"""
    # return "192.168.195.179"

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


players_count = 0
players = {
    1: {"id": 1, "wins": 0, "choice": None, "enemy": 2},
    2: {"id": 2, "wins": 0, "choice": None, "enemy": 1},
}

win_states = {
    "rock": {"win": "scissors"},
    "paper": {"win": "rock"},
    "scissors": {"win": "paper"}
}

player_one_reset = False
player_two_reset = False


# Cuando un cliente se conecta, se le asigna un número de jugador
def connection():
    global players_count
    players_count += 1

    print(f"Client {players_count} connected")

    return players_count


def disconnect(player):
    global players_count

    players_count -= 1
    players[1]["choice"] = None
    players[2]["choice"] = None

    print(f"Client {player} disconnected")


# Cuando un cliente envía su elección, se guarda en una variable global
def send_choice(player, choice):
    global players

    print("Choice received")

    players[player]["choice"] = choice

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

def reset_choice(player):
    global players

    players[player]["choice"] = None

    return "reset"


# Definir la lógica del juego
def get_result(player):
    global players_count, players

    actual_player = players[player]
    enemy_player = players[actual_player["enemy"]]

    if not all([players[1]["choice"], players[2]["choice"]]):
        return {'result': "waiting", 'winner': 'none'}

    if players[1]["choice"] == players[2]["choice"]:
        result = "draw"
    elif win_states[actual_player["choice"]]["win"] == enemy_player["choice"]:
        result = "You win"
        players[player]["wins"] += 1
    else:
        result = "You lose"

    # Checar ganador final
    final_winner = 'none'
    if result == "You win" and players[player]["wins"] == 3:
        final_winner = player["id"]
    elif result == "You lose" and players[enemy_player["id"]]["wins"] == 2:
        final_winner = enemy_player["id"]


    return { 'result': result, 'winner': final_winner, 'wins': players[player]["wins"]}


# Crear el servidor RPC
server = SimpleXMLRPCServer((get_ip_address(), 8000))
print(f"Server running on {get_ip_address()}:8000")

# Registrar las funciones RPC del juego
server.register_function(connection, "connection")
server.register_function(disconnect, "disconnect")
server.register_function(send_choice, "send_choice")
server.register_function(get_result, "get_result")
server.register_function(reset_choice, "reset_choice")

# Servidor
server.serve_forever()
