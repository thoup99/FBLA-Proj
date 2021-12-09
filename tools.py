from tkinter import * ## documentation https://docs.python.org/3/library/tk.html
from datetime import datetime ## documentation https://docs.python.org/3/library/datetime.html

def screenAdjFont(root):
    """Returns the recommended font size based on the screens height"""
    return(round(root.winfo_screenheight() / 98.18))

def screenAdjPadxMult(root):
    """Returns the multiplier required to make widgets fit the screen on the X axis or width"""
    return(root.winfo_screenwidth() / 174.54 / 11)

def screenAdjPadyMult(root):
    """Returns the multiplier required to make widgets fit the screen on the Y axis or height"""
    return(root.winfo_screenheight() / 98.18 / 11)

def setDefaults(root):
    payload = '{"font": {"size": '+str(screenAdjFont(root))+', "name": "Helvetica", "isBold": true}, "colorScheme": "Default", "autoDay": true}'
    with open('./config.json', "w") as file:
        file.write(payload)

def widgetUpdate(root, fontData, colorData) -> None:
    """Updates widgets in desired location with given font and color data"""
    #Constructs font
    if (fontData["isBold"]):
        sFont = (fontData["name"], fontData["size"], "bold")
        largeFont = (fontData["name"], fontData["size"] + 4, "bold")
    else: 
        sFont = (fontData["name"], fontData["size"], "normal")
        largeFont = (fontData["name"], fontData["size"] + 4)
    #Changes font and colors
    root.config(bg= colorData["bg"])
    for widget in root.winfo_children():
        updateInstance(root, widget, colorData, sFont, largeFont)


def updateInstance(root, widget, colorData, Font, lFont):
    if(isinstance(widget, LabelFrame)):
        widget.config(bg= colorData["bg"])
        widget.config(font= Font)
        widget.config(fg= colorData["text"])
        for subWidget in widget.winfo_children():
            updateInstance(root, subWidget, colorData, Font, lFont)
    elif(isinstance(widget, Label)):
            widget.config(bg= colorData["bg"], 
                fg= colorData["text"], 
                font= Font)
    elif(isinstance(widget, OptionMenu)):
        widget.config(font= Font,
            bg= colorData["secondary"],
            fg= colorData["text"],
            highlightbackground= colorData["bg"], 
            highlightcolor= colorData["bg"],
            activebackground= colorData["primary"],
            activeforeground= colorData["text"])
        widget['menu'].config(bg= colorData["secondary"], fg= colorData["text"], font= Font)
    elif(isinstance(widget, Button)):
        widget.config(font= Font,
            bg= colorData["primary"],
            fg= colorData["text"],
            activebackground= colorData["secondary"],
            activeforeground= colorData["textDisabled"],
            disabledforeground= colorData["textDisabled"])
    elif(isinstance(widget, Spinbox)):
        widget.config(font= lFont, 
            buttonbackground= colorData["bg"],
            fg= colorData["text"])
        if (colorData["primary"] == "#f33bee" or colorData["primary"] == "#D2A24C"):
            widget.config(font= lFont, 
                fg= colorData["primary"])
    elif(isinstance(widget, Checkbutton)):
        widget.config(font= Font,
                fg= colorData["text"],
                bg= colorData["bg"],
                activeforeground= colorData["text"],
                activebackground= colorData["bg"])                
        if (colorData["primary"] == "#f33bee" or colorData["primary"] == "#D2A24C"):
            widget.config(font= lFont, 
                fg= colorData["primary"])

def getColorScheme(schemeName):
    colors = {
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
    return (colors[schemeName])

def getCurrentDay():
    weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return weekdays[datetime.today().isoweekday()]
