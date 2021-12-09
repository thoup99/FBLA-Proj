from tkinter import * ## documentation https://docs.python.org/3/library/tk.html
from PIL import ImageTk,Image ## documentation https://pillow.readthedocs.io/en/stable/
from info_frame import InfoFrame
from searcher import Searcher

class MainScreen():
    def __init__(self, root: Tk, padxMult, padyMult):
        self.padxMult = padxMult
        self.padyMult = padyMult
        self.infoFrame = InfoFrame(root, 2, 1, 3, 7, padxMult, padyMult)
        self.searcher = Searcher(self.infoFrame)
        
        #Creates and stores 6 labelFrames inside to be used by the criteria
        self.FRAMES = []
        for x in range(7): #Number is how many frames will be created
            self.FRAMES.append(LabelFrame(root, borderwidth=0, highlightthickness=0))  

        ##Defines the criteria Variables
        self.critServiceVar = StringVar() 
        self.critInOutVar = StringVar()
        self.critDayVar = StringVar()
        self.critOpenNumVar = StringVar()
        self.critOpenMerVar = StringVar()
        self.critCloseNumVar = StringVar()
        self.critCloseMerVar = StringVar()
        self.critLocatedVar = StringVar()
        self.critPriceVar =StringVar()

        ##Sets the criteria Variables
        self.critServiceVar.set("Any")
        self.critInOutVar.set("Any")
        self.critDayVar.set("Any")
        self.critOpenNumVar.set("Any")
        self.critOpenMerVar.set("AM")
        self.critCloseNumVar.set("Any")
        self.critCloseMerVar.set("AM")
        self.critLocatedVar.set("Any")
        self.critPriceVar.set("Any")

        ##Criteria Widgets
        self.critService = OptionMenu(self.FRAMES[0], self.critServiceVar, "Any", "Arcade", "Attractions", "Bar", "Brewery", "Food Store", "Hospital", "Hotel", "Ice Cream Parlor", "Movie Theater", "Park", "Restaurant", "Shopping Center")
        self.critInOut = OptionMenu(self.FRAMES[1], self.critInOutVar, "Any", "Both","Indoor", "Outdoor")
        self.critDay = OptionMenu(self.FRAMES[2], self.critDayVar, "Any", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
        self.critOpenNum = OptionMenu(self.FRAMES[3], self.critOpenNumVar, "Any", "24/7", "1", "2", "3", "4","5", "6","7", "8", "9", "10", "11", "12",)
        self.critOpenMer = OptionMenu(self.FRAMES[3], self.critOpenMerVar, "AM", "PM")
        self.critCloseNum = OptionMenu(self.FRAMES[4], self.critCloseNumVar, "Any","1", "2", "3", "4","5", "6","7", "8", "9", "10", "11", "12")
        self.critCloseMer = OptionMenu(self.FRAMES[4], self.critCloseMerVar, "AM", "PM")
        self.critLocated = OptionMenu(self.FRAMES[5], self.critLocatedVar, "Any", "Altoona", "Duncansville", "Hollidaysburg", "Roaring Spring", "Tyrone")
        self.critPrice = OptionMenu(self.FRAMES[6], self.critPriceVar, "Any", "Less than $10", "Less than $25", "Less than $50", "Less than $100", "Less than $150")

        ##Criteria Widget Labels
        self.critServiceLabel = Label(self.FRAMES[0], text="Type of Service")
        self.critInOutLabel = Label(self.FRAMES[1], text="Indoor/Outdoor Facility")
        self.critDayLabel = Label(self.FRAMES[2], text="Days of Operation")
        self.critOpenLabel = Label(self.FRAMES[3], text="Opens By")
        self.critCloseLabel = Label(self.FRAMES[4], text="Closes After")
        self.critLocatedLabel = Label(self.FRAMES[5], text="Location")
        self.critPriceLabel = Label(self.FRAMES[6], text= "Approxiate Price range")

        ##Images
        #loads image
        self.logo_img = ImageTk.PhotoImage(Image.open("./images/logo.png").resize((round(128 * self.padxMult), round(128 * self.padyMult)), Image.ANTIALIAS))
        #sets image
        self.logo = Label(root, image=self.logo_img)

        #Buttons
        self.submitButton = Button(root, text="Search", command=self.Search, padx= 25 * padxMult, pady= 5 * padyMult)
        self.leftButton = Button(root, text="<<", command=self.scrollLeft, padx= 15 * padxMult, pady= 5 * padyMult)
        self.rightButton = Button(root, text=">>", command=self.scrollRight, padx= 15 * padxMult, pady= 5 * padyMult)


        #Info Frame
        self.infoFrameViewing = Label(root)
        
        self.display()
                

    def Search(self):
        """Searches for locations that meet the selected criteria"""
        self.searcher.searchCriteria(self.critServiceVar.get(), self.critInOutVar.get(), self.critDayVar.get(), self.critOpenNumVar.get(), self.critOpenMerVar.get(), self.critCloseNumVar.get(), self.critCloseMerVar.get(), self.critLocatedVar.get(), self.critPriceVar.get())
        self.infoFrame.currentLocation = 0 #Resets the index to 0 so we get the first result first        
        #If nothing met the criteria we disable multiple infoFrame buttons and display the no results image otherwise update infoFrame
        if (len(self.infoFrame.metCriteria) > 0):
            self.frameScrollUpdate()
            self.infoFrame.googleBut.config(state=NORMAL)
            self.infoFrame.update(self.critDayVar.get())
        else:
            self.infoFrame.noResults()
            self.leftButton.config(state= DISABLED)
            self.infoFrameViewing.config(text= "0 of 0")
            self.rightButton.config(state= DISABLED)  

    def scrollLeft(self):
        """Moves to the previous location that meets our criteria"""
        self.infoFrame.currentLocation -= 1
        self.infoFrame.update(self.critDayVar.get())
        self.frameScrollUpdate()

    def scrollRight(self):
        """Moves to the next location that meets our criteria"""
        self.infoFrame.currentLocation += 1
        self.infoFrame.update(self.critDayVar.get())
        self.frameScrollUpdate()

    def frameScrollUpdate(self):
        """Updates the Widgets involved with moving infoFrame slides and displaying the current one we're on"""
        self.leftButton.config(state= NORMAL)
        self.rightButton.config(state= NORMAL)
        if (self.infoFrame.currentLocation == 0):
            self.leftButton.config(state= DISABLED)
        if (self.infoFrame.currentLocation == len(self.infoFrame.metCriteria) - 1):
            self.rightButton.config(state= DISABLED)
        self.infoFrameViewing.config(text= str(self.infoFrame.currentLocation + 1) +" of "+str(len(self.infoFrame.metCriteria)))

    def display(self):
        """Shows Widgets that are currently hiden"""
        pX = (10 * self.padxMult, 0)
        pX2 = (12 * self.padxMult, 0)
        pY = (0, 21 * self.padyMult)
        self.logo.grid(row=0, columnspan = 2, sticky= N+W, padx= (25 * self.padxMult, 0), pady= 25 * self.padyMult)
        for it, frame in enumerate(self.FRAMES):
            frame.grid(row= it+1, sticky= W)
        #Criteria 1
        self.critServiceLabel.grid(row=1, sticky=W, padx= (12 * self.padxMult, 170 * self.padxMult))
        self.critService.grid(row=2, sticky=W, padx=pX, pady= pY)
        #Criteria 2
        self.critInOutLabel.grid(row=1, sticky=W, padx= pX2)
        self.critInOut.grid(row=2, sticky=W, padx=pX, pady= pY)
        #Criteria 3
        self.critDayLabel.grid(row= 1, sticky=W, padx= pX2)
        self.critDay.grid(row=2, sticky=W, padx=pX, pady= pY)
        #Criteria 4
        self.critOpenLabel.grid(row= 1, columnspan= 2, sticky = W, padx= pX2)
        self.critOpenNum.grid(row= 2, sticky = W, padx=pX, pady= pY)
        self.critOpenMer.grid(row=2, column=1, sticky=W, pady= pY)
        #Criteria 5
        self.critCloseLabel.grid(row= 1, columnspan= 2, sticky = W, padx= pX2)
        self.critCloseNum.grid(row= 2, sticky = W, padx=pX, pady= pY)
        self.critCloseMer.grid(row=2, column=1, sticky=W, pady= pY)
        #Criteria 6
        self.critLocatedLabel.grid(row= 1, sticky = W, padx= pX2)
        self.critLocated.grid(row= 2, columnspan= 2, sticky = W, padx=pX, pady= pY)
        #Criteria 7
        self.critPriceLabel.grid(row= 1, sticky = W, padx= pX2)
        self.critPrice.grid(row= 2, columnspan= 2, sticky = W, padx=pX, pady= pY)
        #InfoFrame
        self.infoFrame.display()
        self.submitButton.grid(row=8, pady=20 * self.padyMult)
        self.leftButton.grid(column=2 , row=8, sticky= E)
        self.infoFrameViewing.grid(column=3, row=8)
        self.rightButton.grid(column= 4, row=8, sticky= W)
        
    def hide(self):
        """Hides Widgets that are currently being displayed"""
        self.infoFrame.Frame.grid_remove()
        self.submitButton.grid_remove()
        self.leftButton.grid_remove()
        self.infoFrameViewing.grid_remove()
        self.rightButton.grid_remove()
        #Removes the Frames containing the criteria
        for frame in self.FRAMES:
            frame.grid_remove()
