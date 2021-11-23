from tkinter import *
from PIL import ImageTk,Image
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
        self.criteriaVar1 = StringVar() 
        self.criteriaVar2 = StringVar()
        self.criteriaVar3 = StringVar()
        self.criteriaVar4 = StringVar()
        self.criteriaVar4Mer = StringVar()
        self.criteriaVar5 = StringVar()
        self.criteriaVar5Mer = StringVar()
        self.criteriaVar6 = StringVar()
        self.criteriaVar7 =StringVar()

        ##Sets the criteria Variables
        self.criteriaVar1.set("Any")
        self.criteriaVar2.set("Any")
        self.criteriaVar3.set("Any")
        self.criteriaVar4.set("Any")
        self.criteriaVar4Mer.set("AM")
        self.criteriaVar5.set("Any")
        self.criteriaVar5Mer.set("AM")
        self.criteriaVar6.set("Any")
        self.criteriaVar7.set("Any")

        ##Criteria Widgets
        self.crit1 = OptionMenu(self.FRAMES[0], self.criteriaVar1, "Any", "Arcade", "Attractions", "Bar", "Brewery", "Food Store", "Hospital", "Hotel", "Ice Cream Parlor", "Movie Theater", "Park", "Restaurant", "Shopping Center")
        self.crit2 = OptionMenu(self.FRAMES[1], self.criteriaVar2, "Any", "Both","Indoor", "Outdoor")
        self.crit3 = OptionMenu(self.FRAMES[2], self.criteriaVar3, "Any", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
        self.crit4Num = OptionMenu(self.FRAMES[3], self.criteriaVar4, "Any", "24/7", "1", "2", "3", "4","5", "6","7", "8", "9", "10", "11", "12",)
        self.crit4Meridiem = OptionMenu(self.FRAMES[3], self.criteriaVar4Mer, "AM", "PM")
        self.crit5Num = OptionMenu(self.FRAMES[4], self.criteriaVar5, "Any","1", "2", "3", "4","5", "6","7", "8", "9", "10", "11", "12")
        self.crit5Meridiem = OptionMenu(self.FRAMES[4], self.criteriaVar5Mer, "AM", "PM")
        self.crit6 = OptionMenu(self.FRAMES[5], self.criteriaVar6, "Any", "Altoona", "Duncansville", "Hollidaysburg", "Roaring Spring", "Tyrone")
        self.crit7 = OptionMenu(self.FRAMES[6], self.criteriaVar7, "Any", "Less than $10", "Less than $25", "Less than $50", "Less than $100", "Less than $150")

        ##Criteria Widget Labels
        self.crit1Label = Label(self.FRAMES[0], text="Type of Service")
        self.crit2Label = Label(self.FRAMES[1], text="Indoor/Outdoor Facility")
        self.crit3Label = Label(self.FRAMES[2], text="Days of Operation")
        self.crit4Label = Label(self.FRAMES[3], text="Opens By")
        self.crit5Label = Label(self.FRAMES[4], text="Closes After")
        self.crit6Label = Label(self.FRAMES[5], text="Location")
        self.crit7Label = Label(self.FRAMES[6], text= "Approxiate Price range")

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
        self.searcher.searchCriteria(self.criteriaVar1.get(), self.criteriaVar2.get(), self.criteriaVar3.get(), self.criteriaVar4.get(), self.criteriaVar4Mer.get(), self.criteriaVar5.get(), self.criteriaVar5Mer.get(), self.criteriaVar6.get(), self.criteriaVar7.get())
        self.infoFrame.currentLocation = 0 #Resets the index to 0 so we get the first result first        
        #If nothing met the criteria we disable multiple infoFrame buttons and display the no results image otherwise update infoFrame
        if (len(self.infoFrame.metCriteria) > 0):
            self.frameScrollUpdate()
            self.infoFrame.googleBut.config(state=NORMAL)
            self.infoFrame.update(self.criteriaVar3.get())
        else:
            self.infoFrame.noResults()
            self.leftButton.config(state= DISABLED)
            self.infoFrameViewing.config(text= "0 of 0")
            self.rightButton.config(state= DISABLED)  

    def scrollLeft(self):
        """Moves to the previous location that meets our criteria"""
        self.infoFrame.currentLocation -= 1
        self.infoFrame.update(self.criteriaVar3.get())
        self.frameScrollUpdate()

    def scrollRight(self):
        """Moves to the next location that meets our criteria"""
        self.infoFrame.currentLocation += 1
        self.infoFrame.update(self.criteriaVar3.get())
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
        self.crit1Label.grid(row=1, sticky=W, padx= (12 * self.padxMult, 170 * self.padxMult))
        self.crit1.grid(row=2, sticky=W, padx=pX, pady= pY)
        #Criteria 2
        self.crit2Label.grid(row=1, sticky=W, padx= pX2)
        self.crit2.grid(row=2, sticky=W, padx=pX, pady= pY)
        #Criteria 3
        self.crit3Label.grid(row= 1, sticky=W, padx= pX2)
        self.crit3.grid(row=2, sticky=W, padx=pX, pady= pY)
        #Criteria 4
        self.crit4Label.grid(row= 1, columnspan= 2, sticky = W, padx= pX2)
        self.crit4Num.grid(row= 2, sticky = W, padx=pX, pady= pY)
        self.crit4Meridiem.grid(row=2, column=1, sticky=W, pady= pY)
        #Criteria 5
        self.crit5Label.grid(row= 1, columnspan= 2, sticky = W, padx= pX2)
        self.crit5Num.grid(row= 2, sticky = W, padx=pX, pady= pY)
        self.crit5Meridiem.grid(row=2, column=1, sticky=W, pady= pY)
        #Criteria 6
        self.crit6Label.grid(row= 1, sticky = W, padx= pX2)
        self.crit6.grid(row= 2, columnspan= 2, sticky = W, padx=pX, pady= pY)
        #Criteria 7
        self.crit7Label.grid(row= 1, sticky = W, padx= pX2)
        self.crit7.grid(row= 2, columnspan= 2, sticky = W, padx=pX, pady= pY)
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