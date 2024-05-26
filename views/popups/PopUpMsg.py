from PySide6.QtWidgets import QMessageBox
import time


class PopUpMsg(QMessageBox):
    def __init__(self, title: str, message: str, buttons: QMessageBox.ButtonRole = QMessageBox.NoButton,
                 if_exec: bool = False,
                 parent: None = None):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setStandardButtons(buttons)
        self.if_exec = if_exec
        self.exec_() if if_exec else None

    def show(self):
        """Show the message box for 2 seconds if if_exec is False, otherwise show the message box until the user closes it."""
        if not self.if_exec:
            super().show()
            time.sleep(2)
        else:
            super().show()
