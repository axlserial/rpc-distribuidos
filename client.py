from xmlrpc.client import ServerProxy
from threading import Thread, current_thread
from PyQt5 import QtWidgets, uic
from Dialog import Dialog
from result_dialog import ResultDialog
import sys

# # Conectar al servidor RPC
# server = ServerProxy("http://192.168.1.64:8000/")

# # Obtener el número de player
# player = server.connection()


class Cliente(QtWidgets.QMainWindow):
    def __init__(self):
        super(Cliente, self).__init__()

        self.server = None
        self.player = None
        self.thread = Thread(target=self.listenServer)
        self.result = None
        self.round = 0

        # Cargar la interfaz de usuario
        uic.loadUi("UI/client.ui", self)

        # Bind de los botones
        self.button_ip.clicked.connect(self.iniciar_con)
        self.scissors_button.clicked.connect(lambda _: self.choice_options('scissors'))
        self.paper_button.clicked.connect(lambda _: self.choice_options('paper'))
        self.rock_button.clicked.connect(lambda _: self.choice_options('rock'))
        self.show()
    
    
    
    def listenServer(self):
        print('escuchando', self.player)
        result = self.server.get_result(self.player)
        
        while result['result'] == "waiting":
            result = self.server.get_result(self.player)
            
        self.result = result
        self.server.reset_choice(self.player)
        
        # Actualizamos el número de ronda
        self.round += 1
        self.num_game_label.setText(str(self.round))

        # Ronda ganada
        if result['result'] == 'You win':
            self.round_label.setText('Ganaste la ronda')
            self.score_label.setText(str(result['wins']))

        elif result['result'] == 'You lose':
            self.round_label.setText('Perdiste la ronda')
        else:
            self.round_label.setText('Empate')

        # Partida terminada
        if result['winner'] != 'none':
            ResultDialog(self)
        
        return

    def iniciar_con(self):
        # IP del servidor
        ip = self.input_ip.text()

        # Campo vacio
        if ip == "":
            Dialog("Ingrese una dirección IP", self).exec_()
            return

        # obtenemos la ip y el puerto
        try:
            ip, port = ip.split(":")
        except:
            Dialog("Ingrese una dirección IP válida (IP:PUERTO)", self).exec_()
            return

        # Conectamos con el servidor
        try:
            self.server = ServerProxy(f"http://{ip}:{port}/")
            #self.server.allow_none = True
            self.player = self.server.connection()
        except:
            Dialog("No se pudo conectar con el servidor", self).exec_()
            return

        # Mostramos el mensaje de conexión exitosa
        Dialog("Partida Iniciada", self).exec_()

        # Habilitamos los botones y labels (piedra, papel, tijera)
        
        self.rock_button.setEnabled(True)
        self.paper_button.setEnabled(True)
        self.scissors_button.setEnabled(True)

        self.rock_label.setEnabled(True)
        self.paper_label.setEnabled(True)
        self.scissors_label.setEnabled(True)

        # Deshabilitamos el botón de conectar
        self.button_ip.setEnabled(False)
        self.input_ip.setEnabled(False)

    def choice_options(self, choice):
        # Mandamos la opción que escogio el jugador
        self.server.send_choice(self.player, choice)
        self.thread.start()
        self.thread.join()
    

    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Cliente()
    sys.exit(app.exec_())

#---------------------------------------------------------------------------------------

# def play():
#     while True:
#         global server, player
#         server.reset_choice(player)
#         choice = input("Choose rock, paper or scissors: ")
#         server.send_choice(player, choice)

#         result = server.get_result(player)
#         while result == "waiting":
#             result = server.get_result(player)

#         print(result)

#         wants_to_play = input("Do you want to play again? (y/n): ")
#         if wants_to_play == "n":
#             server.disconnect(player)
#             break


# # Hilo
# thread = Thread(target=play)
# thread.start()
# thread.join()


