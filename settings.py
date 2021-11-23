import json
from tkinter import *
from preview_frame import PreviewFrame
from tools import setDefaults, widgetUpdate, colors
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

        self.fontSelectedVar.trace("w", self.previewFont)
        self.fontSizeVar.trace("w", self.previewFont)
        self.isBoldVar.trace("w", self.previewFont)
        self.colorSchemeVar.trace("w", self.previewColor)

    def saveSettings(self):
        payload = '{"font": {"size": '+self.fontSizeVar.get() + ', "name": "'+self.fontSelectedVar.get()+ '", "isBold": '+str(self.isBoldVar.get()).lower()+'},"colorScheme": "'+ self.colorSchemeVar.get()+'", "autoDay": '+str(self.isAutoDayVar.get()).lower()+'}'
        
        saveJson = json.loads(json.dumps(payload))
        with open("./config.json", "w") as file:
            file.write(saveJson)
        widgetUpdate(self.root)          

    def loadSettings(self):
        with open("./config.json") as jsonData:
            settings = json.load(jsonData)
        self.colorSchemeVar.set(settings["colorScheme"])
        self.fontSizeVar.set(str(settings["font"]["size"]))
        self.fontSelectedVar.set(settings["font"]["name"])
        self.isBoldVar.set(settings["font"]["isBold"])
        self.isAutoDayVar.set(settings["autoDay"])            
    
    def previewFont(self, *args):
        if (self.isBoldVar.get()):
            newFont = (self.fontSelectedVar.get(), int(self.fontSizeVar.get()), 'bold')
        else: newFont = (self.fontSelectedVar.get(), int(self.fontSizeVar.get()))
        self.previewFrame.Frame.config(font= newFont)
        self.previewFrame.text.config(font= newFont)
        self.previewFrame.optionMenu.config(font= newFont)
        self.previewFrame.button.config(font= newFont)    

    def previewColor(self, *args):
        colorData = colors[self.colorSchemeVar.get()]
        self.previewFrame.Frame.config(bg= colorData["bg"],
            fg= colorData["text"])
        self.previewFrame.text.config(bg= colorData["bg"], 
            fg= colorData["text"])
        self.previewFrame.optionMenu['menu'].config(bg= colorData["secondary"], fg= colorData["text"])
        self.previewFrame.optionMenu.config(bg= colorData["secondary"],
            fg= colorData["text"],
            highlightbackground= colorData["bg"], 
            highlightcolor= colorData["bg"],
            activebackground= colorData["primary"],
            activeforeground= colorData["text"])
        self.previewFrame.button.config(bg= colorData["primary"],
            fg= colorData["text"],
            activebackground= colorData["secondary"],
            activeforeground= colorData["textDisabled"],
            disabledforeground= colorData["textDisabled"])

    def restoreDefault(self):
        setDefaults(self.root)
        widgetUpdate(self.root)
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