import pandas as pd
from Station import Station
from signals import (
    trackControllerToTrackModel, 
    trainModelToTrackModel, 
    ctcToTrackModel,
    trackModelToCTC,
    trackModelToTrainModel
)

class TrackData:
    redTrackData = {}
    greenTrackData = {}

    def __init__(self):
        self.redTrackData = self.read_track_data(
            "src\main\TrackModel\Track Layout & Vehicle Data vF2.xlsx", "Red Line"
        )
        self.greenTrackData = self.read_track_data(
            "src\main\TrackModel\Track Layout & Vehicle Data vF2.xlsx", "Green Line"
        )
        
        ctcToTrackModel.requestThroughput.connect(self.get_ticket_sales)
        
        trackControllerToTrackModel.suggestedSpeed.connect(self.set_suggested_speed)
        trackControllerToTrackModel.authority.connect(self.set_authority)
        
        trainModelToTrackModel.sendCurrentPassengers.connect(self.update_station_data)

    def read_track_data(self, filePath, lineName):
        excelData = pd.read_excel(filePath, sheet_name=lineName)
        if lineName == "Red Line":
            data = excelData.head(76).to_dict(orient="records")
        elif lineName == "Green Line":
            data = excelData.head(150).to_dict(orient="records")
        self.initialize_data(data, lineName)
        return data

    def initialize_data(self, data, lineName):
        # Set default values for track
        for block in data:
            block["Failures"] = ["None"]
            block["Occupancy"] = 0
            block["Maintenance"] = 0
            block["Suggested Speed"] = 0
            block["Authority"] = 0
            #Initialize Station Data
            if type(block["Infrastructure"]) == str:
                if "STATION" in block["Infrastructure"]:
                    block["Ticket Sales"] = 0
                    block["Passengers Waiting"] = 0
                    block["Passengers Boarding"] = 0
                    block["Passengers Disembarking"] = 0
                if lineName == "Green Line":
                    if block["Block Number"] == 2:  # Section A, Pioneer
                        block["Beacon"] = {
                            "Next Station1": "STATION",
                            "Next Station2": "",
                            "Current Station": "PIONEER",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 9:  # Section C, Edgebrook
                        block["Beacon"] = {
                            "Next Station1": "PIONEER",
                            "Next Station2": "",
                            "Current Station": "EDGEBROOK",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 16:  # Section D, Station
                        block["Beacon"] = {
                            "Next Station1": "EDGEBROOK",
                            "Next Station2": "WHITED",
                            "Current Station": "STATION",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 22:  # Section F, Whited
                        block["Beacon"] = {
                            "Next Station1": "STAION",
                            "Next Station2": "SOUTH BANK",
                            "Current Station": "WHITED",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 31:  # Section G, South Bank
                        block["Beacon"] = {
                            "Next Station1": "CENTRAL",
                            "Next Station2": "",
                            "Current Station": "SOUTH BANK",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 39:  # Section I, Central
                        block["Beacon"] = {
                            "Next Station1": "INGLEWOOD",
                            "Next Station2": "",
                            "Current Station": "CENTRAL",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 48:  # Section I, Inglewood
                        block["Beacon"] = {
                            "Next Station1": "OVERBROOK",
                            "Next Station2": "",
                            "Current Station": "INGLEWOOD",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 57:  # Section I, Overbrook
                        block["Beacon"] = {
                            "Next Station1": "GLENBURY",
                            "Next Station2": "",
                            "Current Station": "OVERBROOK",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 65:  # Section K, Glenbury
                        block["Beacon"] = {
                            "Next Station1": "DORMONT",
                            "Next Station2": "",
                            "Current Station": "GLENBURY",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 73:  # Section L, Dormont
                        block["Beacon"] = {
                            "Next Station1": "MT LEBANON",
                            "Next Station2": "",
                            "Current Station": "DORMONT",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 77:  # Section N, Mt Lebanon
                        block["Beacon"] = {
                            "Next Station1": "POPULAR",
                            "Next Station2": "DORMONT",
                            "Current Station": "MT LEBANON",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 88:  # Section O, Poplar
                        block["Beacon"] = {
                            "Next Station1": "CASTLE SHANNON",
                            "Next Station2": "MT LEBANON",
                            "Current Station": "POPLAR",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 96:  # Section P, Castle Shannon
                        block["Beacon"] = {
                            "Next Station1": "MT LEBANON",
                            "Next Station2": "",
                            "Current Station": "CASTLE SHANNON",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 105:  # Section T, Dormont
                        block["Beacon"] = {
                            "Next Station1": "GLENBURY",
                            "Next Station2": "",
                            "Current Station": "DORMONT",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 114:  # Section U, Glenbury
                        block["Beacon"] = {
                            "Next Station1": "OVERBROOK",
                            "Next Station2": "",
                            "Current Station": "GLENBURY",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 123:  # Section W, Overbrook
                        block["Beacon"] = {
                            "Next Station1": "INGLEWOOD",
                            "Next Station2": "",
                            "Current Station": "OVERBROOK",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 132:  # Section W, Inglewood
                        block["Beacon"] = {
                            "Next Station1": "CENTRAL",
                            "Next Station2": "",
                            "Current Station": "INGLEWOOD",
                            "Door Side": block["Station Side"],
                        }
                    if block["Block Number"] == 141:  # Section W, Central
                        block["Beacon"] = {
                            "Next Station1": "WHITED",
                            "Next Station2": "",
                            "Current Station": "CENTRAL",
                            "Door Side": block["Station Side"],
                        }

    def set_data(self, line, data):
        if line == "Red":
            self.redTrackData = data
            for block in self.redTrackData:
                print(block["Failures"])
        elif line == "Green":
            self.greenTrackData = data
            for block in self.greenTrackData:
                print(block["Failures"])

    def get_data(self, line):
        if line == "Red":
            return self.redTrackData
        return self.greenTrackData
    
    def set_suggested_speed(self, line, _, blockNum, suggestedSpeed):
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Suggested Speed"] == suggestedSpeed
        if line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Suggested Speed"] == suggestedSpeed
    
    def set_authority(self, line, _, blockNum, authority):
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Authority"] == authority
        if line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Authority"] == authority

    def update_station_data(self, line, stationName, currentPassengers):
        #stationName must be caps
        station = Station()
        
        if line == "Red":
            for block in self.redTrackData:
                if type(block["Infrastructure"]) == str:
                    if stationName in block["Infrastructure"]:
                        ticketSales = station.get_ticket_sales() #random number generated
                        block["Ticket Sales"] += ticketSales
                            
                        waiting = block["Passengers Waiting"] + ticketSales
                        disembarkingPassengers, newPassengers, passengersWaiting = station.get_passenger_exchange(currentPassengers, waiting)
                        
                        block["Passengers Disembarking"] = disembarkingPassengers
                        block["Passengers Boarding"] = newPassengers
                        block["Passengers Waiting"] = passengersWaiting
                        
                        trackModelToTrainModel.newCurrentPassengers.emit(newPassengers)
        elif line == "Green":
            for block in self.greenTrackData:
                if type(block["Infrastructure"]) == str:
                    if stationName in block["Infrastructure"]:
                        ticketSales = station.get_ticket_sales() #random number generated
                        block["Ticket Sales"] += ticketSales
                        
                        waiting = block["Passengers Waiting"] + ticketSales 
                        disembarkingPassengers, newPassengers, passengersWaiting = station.get_passenger_exchange(currentPassengers, waiting)
                        
                        block["Passengers Disembarking"] = disembarkingPassengers
                        block["Passengers Boarding"] = newPassengers
                        block["Passengers Waiting"] = passengersWaiting
                        # print(ticketSales, passengersWaiting, disembarkingPassengers, newPassengers)
                        
                        trackModelToTrainModel.newCurrentPassengers.emit(newPassengers)
                
    def get_ticket_sales(self, line):
        throughput = 0 #Reset
        if line == "Red":
            for block in self.redTrackData:
                if "STATION" in block["Infrastructure"]:
                    throughput += block["Ticket Sales"]
                    block["Ticket Sales"] = 0 #Reset
        elif line == "Green":
            for block in self.greenTrackData:
                if "STATION" in block["Infrastructure"]:
                    throughput += block["Ticket Sales"]
                    block["Ticket Sales"] = 0 #Reset
        trackModelToCTC.throughput.emit(throughput)
