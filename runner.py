from tkinter import *
from mainScreen import MainScreen
from settings import Settings
from tools import *
from os.path import exists
import json

class windowManager():
    def __init__(self, root) -> None:
        self.currentScreen = 0

        self.padx = screenAdjPadxMult(root)
        self.pady = screenAdjPadyMult(root)
        self.mainScreen = MainScreen(root, self.padx, self.pady)
        self.settingsScreen = Settings(root, self.padx, self.pady)

        self.settingsButton = Button(root, text="Settings", command= self.screenSwitcher)
        self.settingsButton.grid(column= 4, row=0, padx= (0, 25 * self.padx), sticky=E)

        with open("config.json") as jsonData:
            configs = json.load(jsonData)
            fontData = configs["font"]
            colorData = getColorScheme(configs["colorScheme"])
            widgetUpdate(root, fontData, colorData)
            if (configs["autoDay"]):
                self.mainScreen.criteriaVar3.set(getCurrentDay())
            self.mainScreen.Search()
            
    def screenSwitcher(self):
        """Handles all action necessary when swithing between the two screen. This includes swithing the screens."""
        #Settings -> MainScreen
        if (self.currentScreen == 1):
            self.settingsScreen.hide()            
            self.mainScreen.display()
            self.currentScreen = 0
        #MainScreen -> Settings
        else:
            #self.root.geometry(self.root.geometry())
            self.mainScreen.hide()
            self.settingsScreen.display()
            self.settingsScreen.loadSettings()
            self.currentScreen = 1

if __name__ == "__main__":
    root = Tk()
    root.title('Blair County Bureau of Tourism')
    root.iconphoto(False, PhotoImage(file="./images/logo.png"))
    if (not exists("./config.json")):
        setDefaults(root)

    wm = windowManager(root)

    root.mainloop()