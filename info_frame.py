from tkinter import *
from PIL import ImageTk,Image
import json
import webbrowser


class InfoFrame():
    def __init__(self, root, pCol, pRow, pColumnspan, pRowspan, padxMult, padyMult):
        self.pCol = pCol
        self.pRow = pRow
        self.pColumnspan = pColumnspan
        self.pRowspan = pRowspan
        self.padxMult = padxMult
        self.padyMult = padyMult
        self.Frame = LabelFrame(root, borderwidth= 4)
        
        self.metCriteria = []
        self.googleLink = ""
        #Acts as an index for our metCriteria
        self.currentLocation = 0
        
        self.noResultsimage = ImageTk.PhotoImage(Image.open('./images/NoResults.jpg'))
        
        ##Creates the widgets we will use
        self.locationImage = ImageTk.PhotoImage(Image.open('./images/NoResults.jpg'))
        self.image = Label(self.Frame, image= self.locationImage)
        self.locName = Label(self.Frame, text= "Location Name")
        self.inOut = Label(self.Frame, text= "In/Outdoor")
        self.tags = Label(self.Frame, text="Tags")
        self.hours = Label(self.Frame, text="Hours")
        self.closedOn = Label(self.Frame, text="Closed On")
        self.location = Label(self.Frame, text="Exact Location")
        self.description = Label(self.Frame, text="Description", justify=LEFT, wraplength=round(522 * self.padxMult))
        self.googleBut = Button(self.Frame, text="Open in Google", command= self.openGoogle ,pady= 8 * self.padyMult, padx= 15 * padxMult)


    def openGoogle(self):
        webbrowser.open(self.googleLink)

    def openFile(self, locName, dataReturned: int):
        """Opens a location file when given its name. Setting dataReturned to 0 returns criteria data and 1 returns frame data. Anything else returns both"""
        with open('./location_info/'+locName) as jsonData:
            returnData = json.load(jsonData)
        if dataReturned == 0:
            return(returnData["criteriaData"])
        elif dataReturned == 1:
            return returnData["frameData"]
        else:
            return returnData
    

    def update(self, day):
        """Updates the information inside of the Frame to match whatever the currently selected location is"""
        #Loads the locations data
        criteriaData = self.openFile(self.metCriteria[self.currentLocation], 0)
        frameData = self.openFile(self.metCriteria[self.currentLocation], 1)
        self.googleLink = frameData["link"]
        #Sets the image and resized it according to the screens size
        self.locationImage = ImageTk.PhotoImage(Image.open('./images/'+self.metCriteria[self.currentLocation][:len(self.metCriteria[self.currentLocation]) - 5]+'.jpg').resize((round(522 * self.padxMult), round(294 * self.padyMult)), Image.ANTIALIAS))
        self.image.config(image= self.locationImage)
        self.image.image = self.locationImage
        self.locName.config(text= frameData["name"])
        if (criteriaData["in/outDoor"] == "Both"):
            self.inOut.config(text= "Services are provided both indoors and outdoors")
        else:
            self.inOut.config(text= "Service is provided "+criteriaData["in/outDoor"]+"s")
        tagText = "Service(s): "
        for tag in criteriaData["service"]:
            tagText += tag +", "
        tagText = tagText[:len(tagText) - 2]
        self.tags.config(text=tagText)
        #Hours
        if (criteriaData["is24/7"]):
            self.hours.config(text="Open 24/7")   
        elif (not self.isSpecialDay(day, criteriaData["specialHours"])): #Checks to see if there are any special hours on our selected day:
            self.hours.config(text="Hours: "+self.militaryToString(criteriaData["hoursOpen"]) +" - "+self.militaryToString(criteriaData["hoursClose"]))
        else:
            #Only gets entered if the selected day has special hours
            self.hours.config(text= self.specialHoursFormat(day, criteriaData["specialHours"], criteriaData["hoursOpen"], criteriaData["hoursClose"]))

        self.closedOn.config(text= "Closed: "+ frameData["closeOn"])
        self.location.config(text= "Located at "+ frameData["location"])
        self.description.config(text= frameData["description"])

    def isSpecialDay(self, day, specialHours) -> bool:
            for sDay in specialHours:
                if (sDay[0] == day):
                    return(True)
            return(False)

    def specialHoursFormat(self, day, specialHours, normalOpen, normalClose) -> str:
        """Formats the hours that will be displayed on the infoframe whenever there are special hours for the selected day"""
        normalOpen = self.militaryToString(normalOpen)
        normalClose = self.militaryToString(normalClose)
        specialOpen = ""
        specialClose = ""
        formatedTime = "Hours: "
        #Formats special open/close if there is one
        for spHour in specialHours:
            if spHour[0] == day and spHour[1] == "open":
                specialOpen = self.militaryToString(spHour[2])
                break
        for spHour in specialHours:
            if spHour[0] == day and spHour[1] == "close":
                specialClose = self.militaryToString(spHour[2])
                break
        #Uses the special hours if any are present otherwise normal ones are used
        if (len(specialOpen) > 0):
            formatedTime += specialOpen
        else:
            formatedTime += normalOpen
        formatedTime += " - "
        if (len(specialClose) > 0):
            return(formatedTime + specialClose)
        else:
            return(formatedTime + normalClose)
        
    def militaryToString(self, time):
        if (time == 0):
            return("12:00 AM")
        if (time >= 1200):
            mer = "PM"
        else: mer = "AM"
        if (time > 1200):
            time -= 1200
            if (time == 0):
                time += 1200
        time = str(time)
        return(time[:len(time) -2] + ":"+time[len(time) -2: ] +" "+mer)


    def noResults(self):
        """When there are no results from the search a special image will be displayed"""
        self.image.config(image= self.noResultsimage)
        self.image.image = self.noResultsimage
        self.locName.config(text= "")
        self.inOut.config(text= "")
        self.tags.config(text= "")
        self.hours.config(text= "")
        self.closedOn.config(text= "")
        self.location.config(text= "")
        self.description.config(text= "")
        self.googleBut.config(state=DISABLED)

    def display(self):
        self.Frame.grid(column= self.pCol, row= self.pRow, columnspan =self.pColumnspan, rowspan= self.pRowspan, sticky= S+N, padx=(0, 20 * self.padxMult))
        self.image.grid(padx= 6 * self.padxMult, pady= 4 * self.padyMult)
        self.locName.grid(row= 1, sticky= W)
        self.tags.grid(row= 2, sticky= W)
        self.hours.grid(row= 3, sticky= W)
        self.closedOn.grid(row = 4, sticky= W)
        self.inOut.grid(row= 5, sticky= W)
        self.location.grid(row= 6, sticky= W)
        self.description.grid(row= 7, sticky= W)
        self.googleBut.grid(row=8, sticky=S, pady=8 * self.padyMult)
        self.googleBut.config(pady= 8 * self.padyMult, padx= 15 * self.padxMult)