import bs4, webbrowser, sys, requests, os, math
#https://www.rwwa.com.au/cris/racefield.aspx?meeting=5154446

class ColSpacingSlot(object):

    def __init__(self, ColSize):
        self.ColSize = ColSize

class MapIt_Bs_Starters_Results(object):
    def __init__(self, Mode, Link):
        #convert meeting link to usable link
        self.ReUseLink = "https://www.rwwa.com.au/cris/raceresults.aspx?meeting=" + Link[50:]
        self.Mode = Mode
        self.PageData = None
        self.headersStarters = ["No", "Horse", "Br", "Trainer", "Rider", "Odds"]
        self.headersResults = ["Placing", "StartPrice", "Br", "Rider", "Trainer"]
        self.headerLengths = []
        self.ColSpacing = []
        self.SetColSpacing()
        self.RefinedData = []
        self.SpacingInfo = []
        self.RawData = None
        self.LocalCycleData = None
        self.WebAddress = self.RequestLink()
        self.MeetingNumber = self.WebAddress[54:]
        self.newLink = self.WebAddress[29:]
        self.finalLink = "https://www.rwwa.com.au/cris/racefield.aspx?meeting=" + self.MeetingNumber
        self.WebAddressField = self.finalLink
        self.Odds = []
        successful = self.RequestData()

        if successful:
            self.DisplayData()
        else:
            self.RequestLink()

    def SetColSpacing(self):
        for i in range(0, 6):
            self.ColSpacing.append(ColSpacingSlot("30"))

    def CheckSetSpacing(self):
        self.CheckHeaders()
        self.CheckContent()

    def CheckHeaders(self):
        #check headers
        countHeader = 0
        selectedArray = self.headersStarters
        if not self.Mode:
            selectedArray = self.headersResults
        count = 0
        for header in selectedArray:
            if len(header) > int(self.ColSpacing[countHeader].ColSize):
                self.ColSpacing[countHeader].ColSize = len(header)
            countHeader += 1

    def CheckContent(self):
        #check content
        for race in self.RefinedData:
            for row in race:
                #print(row)
                for item in row:
                    #print(item)
                    for i in self.ColSpacing:
                        #print(i)
                        if len(item) > int(i.ColSize):
                            i.ColSize = len(item)

    def checkWordSlot(self, word, slotSize):
        offset = len(word) - slotSize
        #print(abs(offset))
        return abs(offset)

    def DisplayData(self):

        self.CheckSetSpacing()

        self.displayContent()

    def displayHeaders(self):
        displayHeaders = ""
        selectedArray = self.headersStarters
        if not self.Mode:
            selectedArray = self.headersResults
        count = 0
        for i in selectedArray:
            #print(int(self.ColSpacing[count].ColSize))
            headerLength = int(self.ColSpacing[count].ColSize)
            self.headerLengths.append(headerLength)
            header = i
            displayHeaders += header

            offset = self.checkWordSlot(header, int(self.ColSpacing[count].ColSize))

            displayHeaders += (' '*offset)
            count += 1
        print(displayHeaders)

    def displayContent(self):
        #print("Place".join([" "] * int(self.ColSpacing[0].ColSize)) + " " + "Horse".join([" "] * int(self.ColSpacing[1].ColSize)) + " " + "Br".join([" "] * int(self.ColSpacing[2].ColSize)) + " " + "Trainer".join([" "] * int(self.ColSpacing[3].ColSize)) + " " + "Rider".join([" "] * int(self.ColSpacing[4].ColSize)) + " " + "Odds".join([" "] * int(self.ColSpacing[5].ColSize)))
        count = 1
        #print("Date: " + str(self.RefinedData))
        count = 0
        for race in self.RefinedData:
            #print(race)
            #Headers
            if self.Mode:
                print(race[1][12:])
            else:
                print(race[1])
                print("----> " + race[2])

            self.displayHeaders()

            rowCount = 0
            for row in race[0]:
                #Content
                #print("Print Row: " + row)
                if self.Mode:
                    place = self.Odds[count][rowCount][1]
                    horse = self.Odds[count][rowCount][2]
                    br = self.Odds[count][rowCount][5]
                    trainer = self.Odds[count][rowCount][8]
                    rider = self.Odds[count][rowCount][9]
                    odds = self.Odds[count][rowCount][10][:5]

                    rowCount += 1
                else:
                    place = row[0]
                    odds = row[1]
                    br = row[4]
                    trainer = row[7]
                    rider = row[8]

                if len(place) > int(self.ColSpacing[0].ColSize):
                    self.ColSpacing[0] = ColSpacingSlot(str(len(place)))

                if self.Mode:
                    if len(horse) > int(self.ColSpacing[1].ColSize):
                        self.ColSpacing[1] = ColSpacingSlot(str(len(horse)))
                else:
                    pass

                if len(br) > int(self.ColSpacing[2].ColSize):
                    self.ColSpacing[2] = ColSpacingSlot(str(len(row[4])))

                if len(trainer) > int(self.ColSpacing[3].ColSize):
                    self.ColSpacing[3] = ColSpacingSlot(str(len(row[7])))

                if len(rider) > int(self.ColSpacing[4].ColSize):
                    self.ColSpacing[4] = ColSpacingSlot(str(len(row[8])))

                if len(odds) > int(self.ColSpacing[5].ColSize):
                    self.ColSpacing[5] = ColSpacingSlot(str(len(row[1])))

                place.ljust(math.ceil(int(self.ColSpacing[0].ColSize)/2))
                place.rjust(math.floor(int(self.ColSpacing[0].ColSize)/2))

                if self.Mode:
                    horse.ljust(math.ceil(int(self.ColSpacing[1].ColSize)/2))
                    horse.rjust(math.floor(int(self.ColSpacing[1].ColSize)/2))
                else:
                    pass

                br.ljust(math.ceil(int(self.ColSpacing[2].ColSize)/2))
                br.rjust(math.floor(int(self.ColSpacing[2].ColSize)/2))

                trainer.ljust(math.ceil(int(self.ColSpacing[3].ColSize)/2))
                trainer.rjust(math.floor(int(self.ColSpacing[3].ColSize)/2))

                rider.ljust(math.ceil(int(self.ColSpacing[4].ColSize)/2))
                rider.rjust(math.floor(int(self.ColSpacing[4].ColSize)/2))

                odds.ljust(math.ceil(int(self.ColSpacing[5].ColSize)/2))
                odds.rjust(math.floor(int(self.ColSpacing[5].ColSize)/2))

                place = str(place).strip("\n").strip("\n\n")

                if self.Mode:
                    horse = horse.strip("\n").strip("\n\n")
                else:
                    pass

                br = str(br).strip("\n").strip("\n\n")
                trainer = trainer.strip("\n").strip("\n\n")
                rider = rider.strip("\n").strip("\n\n")
                odds = odds.strip("\n").strip("\n\n")

                displayString = ""

                if self.Mode:
                    displayString += place
                    offset = self.checkWordSlot(place, int(self.ColSpacing[0].ColSize))
                    displayString += (' '*offset)

                    if self.Mode:
                        displayString += horse
                        offset = self.checkWordSlot(horse, int(self.ColSpacing[1].ColSize))
                        displayString += (' '*offset)
                    else:
                        pass

                    displayString += br
                    offset = self.checkWordSlot(br, int(self.ColSpacing[2].ColSize))
                    displayString += (' '*offset)

                    displayString += trainer
                    offset = self.checkWordSlot(trainer, int(self.ColSpacing[3].ColSize))
                    displayString += (' '*offset)

                    displayString += rider
                    offset = self.checkWordSlot(rider, int(self.ColSpacing[4].ColSize))
                    displayString += (' '*offset)

                    displayString += odds
                    offset = self.checkWordSlot(odds, int(self.ColSpacing[5].ColSize))
                    displayString += (' '*offset)

                else:
                    displayString += place
                    offset = self.checkWordSlot(place, int(self.ColSpacing[0].ColSize))
                    displayString += (' '*offset)

                    displayString += odds
                    offset = self.checkWordSlot(odds, int(self.ColSpacing[5].ColSize))
                    displayString += (' '*offset)

                    displayString += br
                    offset = self.checkWordSlot(br, int(self.ColSpacing[2].ColSize))
                    displayString += (' '*offset)

                    displayString += trainer
                    offset = self.checkWordSlot(trainer, int(self.ColSpacing[3].ColSize))
                    displayString += (' '*offset)

                    displayString += rider
                    offset = self.checkWordSlot(rider, int(self.ColSpacing[4].ColSize))
                    displayString += (' '*offset)

                #displayString = place + (' '*int(self.ColSpacing[0].ColSize))*2 + horse + (' '*int(self.ColSpacing[1].ColSize))*2 + br + (' '*int(self.ColSpacing[2].ColSize))*2 + trainer + (' '*int(self.ColSpacing[3].ColSize))*2 + rider + int((' '*self.ColSpacing[4].ColSize))*2 + odds + (' '*int(self.ColSpacing[5].ColSize))*2
                print(displayString)
                #print("Got Here")
                #print place horse br trainer rider odds
            count += 1

    def RequestLink(self):
        #Change me back before u submit

        link = self.ReUseLink

        #link = "https://www.rwwa.com.au/cris/raceresults.aspx?meeting=5154446"

        linkInvalid = self.CheckLink(link)

        while(linkInvalid):
            print('Invalid input, please try again.')
            link = self.ReUseLink
            linkInvalid = self.CheckLink(link)

        return link

    def CheckLink(self, link):
        if link == "": return True

        if link[0:8] != "https://":
            print("Error no such site!")
            return True

        if(link.find("meeting=") == -1):
            print("Invalid Meeting Number.")
            return True

        return False

    def RequestData(self):

        currentRaceIndex = 0
        while(self.MeetingHasNextRace(currentRaceIndex)):
            currentRaceIndex += 1
            LoopData = self.LocalCycleData
            RefinedLoopData, DayHeader, Dividends = self.RetreiveTableDataFromRaceIndex(currentRaceIndex, LoopData, self.PageData)

            self.RefinedData.append([RefinedLoopData, DayHeader, Dividends])

        currentRaceIndex = 0
        while(self.MeetingHasNextRaceOdds(currentRaceIndex)):
            currentRaceIndex += 1
            LoopDataOdds = self.LocalCycleData
            RefinedLoopData = self.RetreiveTableDataFromRaceIndexOdds(currentRaceIndex, LoopDataOdds, self.PageData)

            self.Odds.append(RefinedLoopData)

        return True

    def RetreiveTableDataFromRaceIndexOdds(self, index, data, pageData):
        tableData = []
        currentRow = []

        rows = []
        for row in data.findAll("tr"):
            #print(row)
            count = 0
            thisRow = []
            for td_txt in row.findAll('td'):
                txt = td_txt.text.lstrip().rstrip()
                #print("-"+txt)
                if count == 11:
                    count = 0
                thisRow.append(td_txt.text.lstrip().rstrip())
                count += 1
            if thisRow != []:
                rows.append(thisRow)

        #print(rows)
        tableData = rows

        return tableData

    def MeetingHasNextRaceOdds(self, index):
        newIndex = index+1
        newRequestLink = self.WebAddressField + "&race=" + str(newIndex)
        #print(newRequestLink)
        response = requests.get(newRequestLink)

        if (response.status_code == 404):
            return False
        try:
            response.raise_for_status()
        except Exception as exc:
            return False

        responseRawData = response.text
        # Beautiful Soup
        racenoSoup = bs4.BeautifulSoup(responseRawData, "html5lib")

        tables = racenoSoup.find_all("table", {"class": "tblcris raceField"})
        self.LocalCycleData = bs4.BeautifulSoup(str(tables), "html5lib")
        self.PageData = racenoSoup
        if len(tables) == 0:
            return False
        return True

    def RetreiveTableDataFromRaceIndex(self, index, data, pageData):
        tableData = []
        currentRow = []

        headerData = pageData.find("span", {"id": "ctl00_ContentPlaceHolderMain_labelHeading"}).get_text()
        dividendData = pageData.find("td", {"id": "ctl00_ContentPlaceHolderMain_raceDetailControlInstance_cellPrizePool"}).get_text()

        rows = []
        for row in data.findAll("tr"):
            #print(row)
            count = 0
            thisRow = []
            for td_txt in row.findAll('td'):
                txt = td_txt.text.lstrip().rstrip()
                #print("-"+txt)
                if count == 13:
                    count = 0
                thisRow.append(td_txt.text.lstrip().rstrip())
                count += 1
            if thisRow != []:
                rows.append(thisRow)

        #print(rows)
        tableData = rows

        return tableData, headerData, dividendData

    def MeetingHasNextRace(self, index):
        newIndex = index+1
        newRequestLink = self.WebAddress + "&race=" + str(newIndex)
        response = requests.get(newRequestLink)

        if (response.status_code == 404):
            return False
        try:
            response.raise_for_status()
        except Exception as exc:
            return False

        responseRawData = response.text
        # Beautiful Soup
        racenoSoup = bs4.BeautifulSoup(responseRawData, "html5lib")

        tables = racenoSoup.find_all("table", {"class": "tblcris tbldata"})
        self.LocalCycleData = bs4.BeautifulSoup(str(tables), "html5lib")
        self.PageData = racenoSoup
        if len(tables) == 0:
            return False
        return True


if len(sys.argv) > 1:
    link = str(sys.argv[1])
else:
    link = input("Please enter a race address: ")

#print("#                         #")

print("Starters:")
instance1 = MapIt_Bs_Starters_Results(True, link)
#print(str(instance1.RefinedData))

#print("#                         #")
#print("#                         #")


print("Results:")
instance2 = MapIt_Bs_Starters_Results(False, link)
#print(str(instance2.RefinedData))

#print("#                        #")
