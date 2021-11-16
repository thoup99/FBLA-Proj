if __name__ == "__main__":
    from tkinter import *
    from mainScreen import MainScreen
    from settings import Settings
    from tools import *
    from os.path import exists

    root = Tk()
    root.title('Blair County Bureau of Tourism')
    root.iconphoto(False, PhotoImage(file="./images/logo.png"))
    if (not exists("./config.json")):
        setDefaults(root)
    padx = screenAdjPadxMult(root)
    pady = screenAdjPadyMult(root)
    mScreen = MainScreen(root, padx, pady)
    sScreen = Settings(root, mScreen, padx, pady)
    widgetUpdate(root)

    root.mainloop()