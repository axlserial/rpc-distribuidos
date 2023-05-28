from PyQt5 import QtWidgets, uic
from Dialog import Dialog
import sys
import os

from xmlrpc.client import ServerProxy


class Cliente(QtWidgets.QMainWindow):
    def __init__(self):
        super(Cliente, self).__init__()

        self.client = None

        # Cargar la interfaz de usuario
        uic.loadUi("client.ui", self)

        # Bind de los botones
        self.button_ip.clicked.connect(self.iniciar_con)
        self.solicitar_btn.clicked.connect(self.solicitar_archivo)

        self.show()

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
            self.client.connect(ip, int(port))
        except:
            Dialog("No se pudo conectar con el servidor", self).exec_()
            return

        # Mostramos el mensaje de conexión exitosa
        Dialog("Conexión exitosa", self).exec_()

        # Habilitamos los botones de solicitar archivo
        self.group_solicitar.setEnabled(True)
        self.solicitar_btn.setEnabled(True)
        self.input_file_name.setEnabled(True)

        # Deshabilitamos el botón de conectar
        self.button_ip.setEnabled(False)
        self.input_ip.setEnabled(False)

    def solicitar_archivo(self):
        # Nombre del archivo
        filename = self.input_file_name.text()

        # Campo vacio
        if filename == "":
            Dialog(
                "Ingrese un nombre de archivo con extensión (archivo.ext)", self
            ).exec_()
            return

        # Enviamos el nombre del archivo al servidor
        self.client.sendMessage(filename)

        # Recibimos la respuesta del servidor
        result = self.client.receiveFile(f"Recived/{filename}")

        # Recibimos el archivo
        if result:
            Dialog("Archivo recibido", self).exec_()
            os.startfile(f"{os.getcwd()}/Recived/{filename}")
        else:
            Dialog("El archivo solicitado no existe", self).exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Cliente()
    sys.exit(app.exec_())
