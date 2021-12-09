import json
from tkinter import *
from preview_frame import PreviewFrame
from tools import getColorScheme, setDefaults, widgetUpdate
class Settings():
    def __init__(self, root, padxMult, padyMult):
        self.root = root
        self.padxMult = padxMult
        self.padyMult = padyMult
        self.previewFrame = PreviewFrame(root, 4, 2, 1, 10, padxMult, padyMult)

        #Variable Storage
        self.colorSchemeVar = StringVar()
        self.fontSelectedVar = StringVar()
        self.isBoldVar = BooleanVar()
        self.fontSizeVar = StringVar()
        self.isAutoDayVar = BooleanVar()

        #Label Creation
        self.colorSchemePrompt = Label(root, text="Color Scheme")
        self.fontSelectedPrompt = Label(root, text="Selected Font")
        self.fontPromt = Label(root, text="Font Size")
        

        #Interactable Widget Creation
        self.colorScheme = OptionMenu(root, self.colorSchemeVar, "Default", "Fall", "High Contrast", "Retro", "Sunset")
        self.fontSize = Spinbox(root, from_=5, to= 16, textvariable=self.fontSizeVar, state= "readonly", width= 5)
        self.fontSelected = OptionMenu(root, self.fontSelectedVar, "Arial Black", "Calibri", "Helvetica", "Tahoma","Times New Roman", "Verdana")
        self.isBold = Checkbutton(root, text= "Bold", variable= self.isBoldVar)
        self.defaultsButton = Button(root, text="Restore Defaults", command=self.restoreDefault, padx= 25 * padxMult, pady= 5 * padyMult)
        self.saveButton = Button(root, text="Save", command=self.saveSettings, padx= 25 * padxMult, pady= 5 * padyMult)
        self.isAutoDay = Checkbutton(root, text="Autofill Day" ,variable= self.isAutoDayVar, )

        ##Updates the preview frame when a setting is changed
        self.fontSelectedVar.trace("w", self.previewUpdate)
        self.fontSizeVar.trace("w", self.previewUpdate)
        self.isBoldVar.trace("w", self.previewUpdate)
        self.colorSchemeVar.trace("w", self.previewUpdate)

    def saveSettings(self):
        payload = '{"font": {"size": '+self.fontSizeVar.get() + ', "name": "'+self.fontSelectedVar.get()+ '", "isBold": '+str(self.isBoldVar.get()).lower()+'},"colorScheme": "'+ self.colorSchemeVar.get()+'", "autoDay": '+str(self.isAutoDayVar.get()).lower()+'}'
        
        with open("./config.json", "w") as file:
            file.write(payload)
        with open("./config.json") as jsonData:
            configs = json.load(jsonData)
            widgetUpdate(self.root, configs["font"], getColorScheme(configs["colorScheme"]))
            
    def loadSettings(self):
        with open("./config.json") as jsonData:
            settings = json.load(jsonData)
        self.colorSchemeVar.set(settings["colorScheme"])
        self.fontSizeVar.set(str(settings["font"]["size"]))
        self.fontSelectedVar.set(settings["font"]["name"])
        self.isBoldVar.set(settings["font"]["isBold"])
        self.isAutoDayVar.set(settings["autoDay"])            

    def previewUpdate(self, *args):
        newFont = {
            "size": int(self.fontSizeVar.get()),
            "name": self.fontSelectedVar.get(), 
            "isBold": self.isBoldVar.get()
        }
        widgetUpdate(self.previewFrame.Frame, newFont, colorData = getColorScheme(self.colorSchemeVar.get()))

    def restoreDefault(self):
        setDefaults(self.root)
        with open("./config.json") as jsonData:
            configs = json.load(jsonData)
            widgetUpdate(self.root, configs["font"], getColorScheme(configs["colorScheme"]))
        self.loadSettings()
        

    def hide(self):
        self.colorSchemePrompt.grid_remove()
        self.colorScheme.grid_remove()
        self.fontSelectedPrompt.grid_remove()
        self.fontSelected.grid_remove()
        self.fontPromt.grid_remove()
        self.fontSize.grid_remove()
        self.isBold.grid_remove()
        self.defaultsButton.grid_remove()
        self.saveButton.grid_remove()
        self.isAutoDay.grid_remove()
        self.previewFrame.Frame.grid_remove()

    def display(self):
        pY = (0, 21 * self.padyMult)
        self.colorSchemePrompt.grid(row=1, padx= (12 * self.padxMult, 134 * self.padxMult), sticky= W)
        self.colorScheme.grid(row= 2, padx= 10 * self.padxMult, pady = pY, sticky= W)
        self.fontSelectedPrompt.grid(row= 4, padx= 12 * self.padxMult, sticky= W)
        self.fontSelected.grid(row= 5, padx= 10 * self.padxMult, pady = pY,sticky= W)
        self.fontPromt.grid(row= 7, padx= 12 * self.padxMult, sticky= W)
        self.fontSize.grid(row= 8, padx= 10 * self.padxMult, pady = pY,sticky= W)
        self.isBold.grid(row= 10, padx= 10 * self.padxMult, sticky= W)
        self.isAutoDay.grid(row= 11, padx= 10 * self.padxMult, sticky= W)
        self.defaultsButton.grid(row= 12, pady=20 * self.padyMult, padx= (0, 25 * self.padxMult), sticky=E+S)
        self.saveButton.grid(column= 4,row=12, pady=(41 * self.padyMult, 20 * self.padyMult), padx= (0, 25 * self.padxMult), sticky=E+S)
        self.previewFrame.Frame.grid()
