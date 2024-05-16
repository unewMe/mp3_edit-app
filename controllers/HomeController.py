from views.HomeView import HomeView
from cores.HomeCore import HomeCore

class HomeController:
    def __init__(self):
        self.view = HomeView()
        self.core = HomeCore()

    def show(self):
        self.view.show()

