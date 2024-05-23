from PySide6.QtWidgets import QMessageBox
import time
class PopUpMsg(QMessageBox):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setStandardButtons(QMessageBox.NoButton)

    def show(self):
        super().show()
        time.sleep(2)
