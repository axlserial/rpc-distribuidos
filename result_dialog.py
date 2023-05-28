from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5 import uic

class ResultDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Partida Terminada")

        uic.loadUi("UI/dialog.ui", self)

        self.exit_button = QDialogButtonBox(QDialogButtonBox.Ok)
        self.exit_button.accepted.connect(self.accept)
        self.exit_button.rejected.connect(self.reject)