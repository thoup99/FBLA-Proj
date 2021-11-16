from tkinter import *

class PreviewFrame():
    def __init__(self, root, pColumn, pRow, pColumnSpan, pRowSpan, padxMult, padyMult) -> None:
        self.Frame = LabelFrame(root, borderwidth= 4, text="Preview")
        self.Frame.grid(column= pColumn, row= pRow, columnspan= pColumnSpan, rowspan= pRowSpan, sticky=N+S,  padx= (0, 25 * padxMult))
        self.Frame.grid_remove()

        self.pY = 21 * padyMult
        self.text = Label(self.Frame, text= "Text")
        self.opMVar = StringVar()
        self.optionMenu = OptionMenu(self.Frame, self.opMVar, "Option 1", "Option 2", "Option 3")
        self.opMVar.set("Option 1")
        self.button = Button(self.Frame, text= "Button")

        self.text.grid(row= 1, pady=self.pY)
        self.optionMenu.grid(row= 2, pady=self.pY, padx=25 * padxMult)
        self.button.grid(row= 3, pady=self.pY)