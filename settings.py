import json
from tkinter import *
from preview_frame import PreviewFrame
from tools import setDefaults, widgetUpdate
class Settings():
    def __init__(self, root, padxMult, padyMult):
        self.root = root
        self.padxMult = padxMult
        self.padyMult = padyMult
        self.previewFrame = PreviewFrame(root, 4, 2, 1, 9, padxMult, padyMult)
        self.colors = {
            "Default": {
                "primary": "#5588FF",
                "secondary": "#91BAD6",
                "bg": "#EBEDF3",
                "text": "#000000",
                "textDisabled": "#666666"
            },
            "High Contrast": {
                "primary": "#f33bee",
                "secondary": "#f33bee",
                "bg": "#000000",
                "text": "#FFFFFF",
                "textDisabled": "#000000"
            },
            "Fall": {
                "primary": "#F3BC2E",
                "secondary": "#D45B12",
                "bg": "#603C14",
                "text": "#000000",
                "textDisabled": "#9C2706"
            },
            "Sunset": {
                "primary": "#DC5563",
                "secondary": "#6C5B7B",
                "bg": "#355C7D",
                "text": "#FF9506",
                "textDisabled": "#C06C84"
            },
            "Retro": { #https://www.figma.com/community/file/1004727401971389237
                "primary": "#D2A24C",
                "secondary": "#CC6B49",
                "bg": "#6F5643",
                "text": "#ECE6C2",
                "textDisabled": "#73BDAB"
            }
        }
        

        


        #Variable Storage
        self.colorSchemeVar = StringVar()
        self.fontSelectedVar = StringVar()
        self.isBoldVar = BooleanVar()
        self.fontSizeVar =StringVar()

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

        self.fontSelectedVar.trace("w", self.previewFont)
        self.fontSizeVar.trace("w", self.previewFont)
        self.isBoldVar.trace("w", self.previewFont)
        self.colorSchemeVar.trace("w", self.previewColor)

    def saveSettings(self):
        sColor = self.colors[self.colorSchemeVar.get()]
        payload = '{"font": {"size": '+self.fontSizeVar.get() + ', "name": "'+self.fontSelectedVar.get()+ '", "isBold": '+str(self.isBoldVar.get()).lower()+'},"color": {"name": "'+self.colorSchemeVar.get()+ '", "primary": "'+sColor["primary"]+'", "secondary": "'+sColor["secondary"]+ '", "bg": "'+sColor["bg"]+ '", "text": "'+sColor["text"]+ '", "textDisabled": "'+sColor["textDisabled"]+'"} }'
        
        saveJson = json.loads(json.dumps(payload))
        with open("./config.json", "w") as file:
            file.write(saveJson)
        #self.mainScreen.infoFrame.description.config(wraplength=round(522 * self.padxMult))   
        widgetUpdate(self.root)
          

    def loadSettings(self):
        with open("./config.json") as settings:
            settings = json.load(settings)
        self.colorSchemeVar.set(settings["color"]["name"])
        self.fontSizeVar.set(str(settings["font"]["size"]))
        self.fontSelectedVar.set(settings["font"]["name"])
        self.isBoldVar.set(settings["font"]["isBold"])        

    
    
    def previewFont(self, *args):
        if (self.isBoldVar.get()):
            nFont = (self.fontSelectedVar.get(), int(self.fontSizeVar.get()), 'bold')
        else: nFont = (self.fontSelectedVar.get(), int(self.fontSizeVar.get()))
        self.previewFrame.Frame.config(font= nFont)
        self.previewFrame.text.config(font= nFont)
        self.previewFrame.optionMenu.config(font= nFont)
        self.previewFrame.button.config(font= nFont)    

    def previewColor(self, *args):
        colorData = self.colors[self.colorSchemeVar.get()]
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
        self.defaultsButton.grid(row= 12, pady=20 * self.padyMult, padx= (0, 25 * self.padxMult), sticky=E+S)
        self.saveButton.grid(column= 4,row=12, pady=(41 * self.padyMult, 20 * self.padyMult), padx= (0, 25 * self.padxMult), sticky=E+S)
        self.previewFrame.Frame.grid()