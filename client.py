from xmlrpc.client import ServerProxy
from threading import Thread
from PyQt5 import QtWidgets, uic
from Dialog import Dialog
import sys

class Cliente(QtWidgets.QMainWindow):
    def __init__(self):
        super(Cliente, self).__init__()

        self.server = None
        self.player = None
        self.thread = None
        self.result = None
        self.round = 0

        # Cargar la interfaz de usuario
        uic.loadUi("UI/client.ui", self)

        # Bind de los botones
        self.button_ip.clicked.connect(self.start_game)
        self.scissors_button.clicked.connect(lambda _: self.choice_options('scissors'))
        self.paper_button.clicked.connect(lambda _: self.choice_options('paper'))
        self.rock_button.clicked.connect(lambda _: self.choice_options('rock'))
        self.show()
    

    def enable_game_buttons(self):
        self.rock_button.setEnabled(True)
        self.paper_button.setEnabled(True)
        self.scissors_button.setEnabled(True)

        self.rock_label.setEnabled(True)
        self.paper_label.setEnabled(True)
        self.scissors_label.setEnabled(True)
    
    def disable_game_buttons(self):
        self.rock_button.setEnabled(False)
        self.paper_button.setEnabled(False)
        self.scissors_button.setEnabled(False)

        self.rock_label.setEnabled(False)
        self.paper_label.setEnabled(False)
        self.scissors_label.setEnabled(False)
        
    def listenServer(self):
        self.round_label.setText('Esperando al otro jugador...')

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
        if result['winner'] != 0:
            if result['winner'] == self.player:
                self.round_label.setText('GANASTE LA PARTIDA!!!')
            else:
                self.round_label.setText('PERDISTE LA PARTIDA :c')
            self.disable_game_buttons()
        else:
            self.enable_game_buttons()
        
        return

    def start_game(self):
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
        self.enable_game_buttons()

        # Deshabilitamos el botón de conectar
        self.button_ip.setEnabled(False)
        self.input_ip.setEnabled(False)

    def choice_options(self, choice):
        # Mandamos la opción que escogio el jugador
        self.server.send_choice(self.player, choice)
        self.thread = Thread(target=self.listenServer)
        self.thread.start()

        # Deshabilitamos los botones y labels (piedra, papel, tijera)
        self.disable_game_buttons()
    

    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Cliente()
    sys.exit(app.exec_())
