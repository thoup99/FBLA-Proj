from tkinter import *
from mainScreen import MainScreen
from settings import Settings
from tools import *
from os.path import exists

class windowManager():
    def __init__(self, root) -> None:
        self.currentScreen = 0

        self.padx = screenAdjPadxMult(root)
        self.pady = screenAdjPadyMult(root)
        self.mScreen = MainScreen(root, self.padx, self.pady)
        self.sScreen = Settings(root, self.padx, self.pady)

        self.settingsButton = Button(root, text="Settings", command= self.screenSwitcher)
        self.settingsButton.grid(column= 4, row=0, padx= (0, 25 * self.padx), sticky=E)

        widgetUpdate(root)

    def screenSwitcher(self):
        """Handles all action necessary when swithing between the two screen. This includes swithing the screens."""
        #Settings -> MainScreen
        if (self.currentScreen == 1):
            self.sScreen.hide()            
            self.mScreen.display()
            self.currentScreen = 0
        #MainScreen -> Settings
        else:
            #self.root.geometry(self.root.geometry())
            self.mScreen.hide()
            self.sScreen.display()
            self.sScreen.loadSettings()
            self.currentScreen = 1

if __name__ == "__main__":
    root = Tk()
    root.title('Blair County Bureau of Tourism')
    root.iconphoto(False, PhotoImage(file="./images/logo.png"))
    if (not exists("./config.json")):
        setDefaults(root)

    wm = windowManager(root)

    root.mainloop()