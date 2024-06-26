import sys

from PySide6.QtWidgets import QApplication

from controllers.HomeController import HomeController
from views.HomeView import HomeView


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = HomeController()
    controller.show()
    sys.exit(app.exec())
