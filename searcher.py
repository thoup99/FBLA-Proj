import os ##documentation https://docs.python.org/3/library/os.html
class Searcher():
    def __init__(self, infoFrame) -> None:
        self.infoFrame = infoFrame
        self.LOCATIONS = os.listdir('./location_info/')#grabs all the file names and puts them in a list

    def searchCriteria(self, serviceIN, inOutDoorIN, openDayIN, openHourIN, openMerIN, closeHourIN, closeMerIn, locatedIN, priceIN) -> None:
        self.infoFrame.metCriteria = []
        for item in self.LOCATIONS:
            locationData = self.infoFrame.openFile(item, 0)
            if(self.testService(serviceIN, locationData["service"])):
                if(self.testInOutDoor(inOutDoorIN, locationData["in/outDoor"])):
                    if(self.testOpenDays(openDayIN, locationData["openDays"])):
                        if(self.testOpenHour(openHourIN, openMerIN, locationData["hoursOpen"], openDayIN, locationData["specialHours"], locationData["is24/7"])):
                            if(self.testCloseHour(closeHourIN, closeMerIn, locationData["hoursClose"], locationData["hoursOpen"], openDayIN, locationData["specialHours"], locationData["hoursOpen"], locationData["is24/7"])):
                                if(self.testLocated(locatedIN, locationData["location"])):
                                    if(self.testPrice(priceIN, locationData["price"])):
                                        self.infoFrame.metCriteria.append(item)

    def testService(self, service, LDservice):
        if (service == "Any" or service in LDservice):
            return(True)
        return(False)
    
    def testInOutDoor(self, inOutDoor, LDinOutDoor):
        if (inOutDoor == "Any" or LDinOutDoor == "Both" or inOutDoor == LDinOutDoor):
            return(True)
        return(False)

    def testOpenDays(self, openDays, LDopenDays):
        if (openDays == "Any" or openDays in LDopenDays):
            return(True)
        return(False)

    def testOpenHour(self, openHour, openMer, LDhoursOpen, day, specialHours, alwaysOpen: bool):
        #checks if we selected 24/7 and if always open is true. Also checks if we dont care when they open
        if (openHour == "Any" or (openHour == "24/7" and alwaysOpen == True)):
            return(True)
        if(openHour == "24/7"):
            return(False)
        openTime = self.toMilitary(openHour, openMer) 
        if (len(specialHours) != 0): #We want to check if the selected day has special hours first
            for spHour in specialHours:
                #if the special hours happen on our selected day
                if (spHour[0] == day and spHour[1] == "open"):
                    print("returning special hours")
                    return(spHour[2] <= openTime)
        return(LDhoursOpen <= openTime)

    def testCloseHour(self, selectedCloseHour, selectedCloseMer, locationCloseHour, locationOpenHour, day, specialHours, openHour, alwaysOpen):
        #Checks if the test need to be run
        if (selectedCloseHour == "Any" or (openHour == "24/7" and alwaysOpen) or alwaysOpen):
            return(True)
        if(openHour == "24/7"):
            return(False)
        searchCloseTime = self.toMilitary(selectedCloseHour, selectedCloseMer) #Converts to military time for easy comparisons(Time selected by the user)
        
        if (len(specialHours) != 0): #We want to check if the selected day has special hours first
            for spHour in specialHours:
                #if the special hours happen on our selected day
                if (spHour[0] == day and spHour[1] == "close"):
                    if (spHour[2] < locationOpenHour): ##Locations that close at or after midnight
                        if (searchCloseTime < locationOpenHour):
                            return(spHour[2] + 2400 > searchCloseTime + 2400)
                        else:
                            return(spHour[2] + 2400 > searchCloseTime)
                    return (spHour[2] > searchCloseTime)

        if (locationCloseHour < locationOpenHour): ##Locations that close at or after midnight
            if (searchCloseTime < locationOpenHour):
                return(locationCloseHour + 2400 > searchCloseTime + 2400)
            else:
                return(locationCloseHour + 2400 > searchCloseTime)
        return(locationCloseHour > searchCloseTime)

    def testLocated(self, located, LDlocated) -> bool:
        if (located == "Any" or located == LDlocated):
            return(True)
        return(False)

    def testPrice(self, price, LDprice) -> bool:
        if (price == "Any"):
            return(True)
        price = int(price[11:])
        if (LDprice <= price):
            return(True)
        return(False)

    def toMilitary(self, hours, meridian) -> int:
        "When given an hour and meridian(AM/PM) returns in military time"
        converted = int(hours)
        if (hours == "12"):
            converted = 0
        converted *= 100
        if (meridian == "PM"):
            converted += 1200
        return(converted)
