from decimal import DivisionByZero
from operator import length_hint
from re import T
import sys
from turtle import Turtle
from PyQt5 import QtGui
from PyQt5.QtCore import QCoreApplication, QRect, QSize, Qt, QTimer, QTime, QDateTime
from PyQt5.QtGui import QCursor, QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QCheckBox,
)
from numpy import block
from qtwidgets import AnimatedToggle
from .TrainModel_Functions import *
from .TrainModel_Calculations import *
# from .TrainModel_Functions import *
# from .TrainModel_Calculations import *

sys.path.append("../../main")
from signals import (
    trainControllerSWToTrainModel,
    trackModelToTrainModel,
    trainModelToTrainController,
    trainModelToTrackModel,
    masterSignals,
)


class TrainModel(QMainWindow):
    # Font variables
    textFontSize = 10
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = "Product Sans"

    # Color variables
    colorDarkBlue = "#085394"
    colorLightRed = "#EA9999"
    colorLightBlue = "#9FC5F8"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"
    colorBlack = "#000000"

    # Dimensions
    w = 960
    h = 960
    moduleName = "Train Model"

    def __init__(self):
        super().__init__()
        self.trainsList = []
        self.functionsInstance = Calculations()

        self.time_interval = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update
        )  # Connect the timer to the update_text function
        self.timer.start(
            self.time_interval
        )  # Update the text every 1000 milliseconds (1 second)

        self.sysTime = QDateTime.currentDateTime()
        self.sysTime.setTime(QTime(0, 0, 0))

        """ Header Template """

        # Setting title
        self.setWindowTitle(self.moduleName)

        # Setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        # Body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet(
            "background-color: white;" "border: 1px solid black"
        )

        # Header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet(
            "background-color:" + self.colorDarkBlue + ";" "border: 1px solid black"
        )

        # Title
        self.titleLabel = QLabel("Train Model", self)
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        title_width = 400
        title_height = 50
        title_x = (self.width() - title_width) // 2
        title_y = 35
        self.titleLabel.setGeometry(title_x, title_y, title_width, title_height)
        self.titleLabel.setStyleSheet("color: white")

        # MTA Logo
        self.pixmapMTALogo = QtGui.QPixmap("src/main/TrainModel/MTA_Logo.png")
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # Module
        self.moduleLabel = QLabel("Train Model", self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # Test bench icon
        self.pixmapGear = QtGui.QPixmap("src/main/TrainModel/gear_icon.png")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # Test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # System time input
        self.systemTimeInput = QLabel("00:00:00", self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet("color:" + self.colorDarkBlue)

        # System time label
        self.systemTimeLabel = QLabel("System Time:", self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed label
        self.systemSpeedLabel = QLabel("System Speed:", self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(689, 140, 200, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed input
        self.systemSpeedInput = QLabel("x1.0", self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)

        # Increase system speed button
        self.pixmapFastForward = QtGui.QPixmap("src/main/TrainModel/fast-forward.svg")
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 143, 20, 20)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # Decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("src/main/TrainModel/rewind.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(819, 143, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        """ Drop-down Menu """

        # Calculate the position of the QComboBox
        drop_down_width = 500
        drop_down_height = 40
        drop_down_x = int((self.w - drop_down_width) // 2)
        drop_down_y = int((self.h / 2) + (self.h / 4) - (drop_down_height / 2))

        # Create the QComboBox
        self.comboBox = QComboBox(self.bodyBlock)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setGeometry(
            QRect(drop_down_x, drop_down_y, drop_down_width, drop_down_height)
        )
        font1 = QFont(self.fontStyle)
        font1.setPointSize(18)
        font1.setKerning(True)
        self.comboBox.setFont(font1)

        # Create a search icon for new window
        self.search_button = QtGui.QPixmap("src/main/TrainModel/search_icon.png")
        self.search_button = self.search_button.scaled(40, 40)
        self.icon = QLabel(self)
        self.icon.setPixmap(self.search_button)
        self.icon.setGeometry(QRect(750, 720, 40, 40))
        self.icon.adjustSize()

        # Connect the search icon to the vehicle class
        self.icon.mousePressEvent = self.open_results_window

        # Insert Train Image to main window
        image_path = "src/main/TrainModel/Train_Image.jpg"
        pixmap_train = QPixmap(image_path)
        image_width = 500
        image_height = 400
        image_y = drop_down_y - image_height - 20
        pixmap_train = pixmap_train.scaled(image_width, image_height)
        train_image_label = QLabel(self.bodyBlock)
        train_image_label.setPixmap(pixmap_train)
        train_image_label.setGeometry(drop_down_x, image_y, image_width, image_height)

        self.retranslate_Ui()

        self.results_window = None

    def retranslate_Ui(self):
        self.setWindowTitle(
            QCoreApplication.translate("TrainModel", "MainWindow", None)
        )
        self.titleLabel.setText(
            QCoreApplication.translate("TrainModel", "Train Model", None)
        )
        self.logo.setText("")

    def open_results_window(self, event):
        # This function is called when the search icon is clicked
        selected_item = self.comboBox.currentText()
        self.results_window = ResultsWindow(
            selected_item, self.trainsList
        )
        self.results_window.show()

    def show_gui(self):
        self.show()

    def signal_period(self, period):
        self.time_interval = period

    def signal_addTrain(self, line, id):
        name = line + "_" + id
        self.trainsList.append(TrainModelAttributes(name))

    def update_drop_down(self):
        existing_items = [self.comboBox.itemText(i) for i in range(self.comboBox.count())]

        all_trainIDs = []
        for trains in self.trainsList:
            all_trainIDs.append(trains.calculations["trainID"])

        missing_trainIDs = set(all_trainIDs) - set(existing_items)
        for trainID in missing_trainIDs:
            self.comboBox.addItem(trainID)

        for item in existing_items:
            if item not in all_trainIDs:
                index = self.comboBox.findText(item)
                self.comboBox.removeItem(index)

    def update(self):
        # system time
        # self.sysTime = self.sysTime.addSecs(1)
        masterSignals.addTrain.emit("green", "train1")
        masterSignals.timingMultiplier.connect(self.signal_period)
        masterSignals.clockSignal.connect(self.sysTime.setTime)
        masterSignals.addTrain.connect(self.signal_addTrain)
        self.timer.setInterval(self.time_interval)

        self.systemTimeInput.setText(self.sysTime.toString("HH:mm:ss"))
        self.systemSpeedInput.setText(
            "x" + format(1 / (self.time_interval / 1000), ".3f")
        )

        self.update_drop_down()
        
        # Signals that connect from the train controller to the train model
        trainControllerSWToTrainModel.sendPower.connect(self.signal_power)
        trainControllerSWToTrainModel.sendDriverEmergencyBrake.connect(self.signal_emergency_brake)
        trainControllerSWToTrainModel.sendDriverServiceBrake.connect(self.signal_brake)
        trainControllerSWToTrainModel.sendAnnouncement.connect(self.signal_announcement)
        trainControllerSWToTrainModel.sendHeadlightState.connect(self.signal_headlights)
        trainControllerSWToTrainModel.sendInteriorLightState.connect(self.signal_interior_lights)
        trainControllerSWToTrainModel.sendLeftDoorState.connect(self.signal_left_door)
        trainControllerSWToTrainModel.sendRightDoorState.connect(self.signal_right_door)
        trainControllerSWToTrainModel.sendSetpointTemperature.connect(self.signal_temperature)
        trainControllerSWToTrainModel.sendAdvertisement.connect(self.signal_advertisements)

        # Signals that connect from the track model to the train model
        trackModelToTrainModel.blockInfo.connect(self.signal_blockInfo)
        trackModelToTrainModel.beacon.connect(self.signal_beacon)
        trackModelToTrainModel.newCurrentPassengers.connect(self.signal_new_passengers)
        
        # Send train controller information
        for trainObject in self.trainsList:
            trainObject.calculations["timeInterval"] = self.time_interval
            self.functionsInstance.power(trainObject)
            self.functionsInstance.temperature(trainObject)
            self.functionsInstance.beacon(trainObject)
            trainModelToTrainController.sendSpeedLimit.emit(trainObject.calculations["trainID"], trainObject.vehicle_status["speed_limit"])
            trainModelToTrainController.sendBlockNumber.emit(trainObject.calculations["trainID"], trainObject.vehicle_status["current_speed"])
            trainModelToTrainController.sendCommandedSpeed.emit(trainObject.calculations["trainID"], trainObject.vehicle_status["commanded_speed"])
            trainModelToTrainController.sendAuthority.emit(trainObject.calculations["trainID"], trainObject.navigation_status["authority"])
            trainModelToTrainController.sendEngineFailure.emit(trainObject.calculations["trainID"], trainObject.failure_status["engine_failure"])
            trainModelToTrainController.sendSignalPickupFailure.emit(trainObject.calculations["trainID"], trainObject.failure_status["signal_pickup_failure"])
            trainModelToTrainController.sendBrakeFailure.emit(trainObject.calculations["trainID"], trainObject.failure_status["brake_failure"])
            trainModelToTrainController.sendPassengerEmergencyBrake.emit(trainObject.calculations["trainID"], trainObject.navigation_status["passenger_emergency_brake"])
            trainModelToTrainController.sendTemperature.emit(trainObject.calculations["trainID"], trainObject.passenger_status["temperature"])
            # trainModelToTrackModel.sendCurrentPassengers.emit(trainObject.calculations["line"], trainObject.calculations["currStation"], trainObject.passenger_status["passengers"])
            trainModelToTrainController.sendNextStation1.emit(trainObject.calculations["trainID"], trainObject.calculations["nextStation1"])
            trainModelToTrainController.sendNextStation2.emit(trainObject.calculations["trainID"], trainObject.calculations["nextStation2"])
            trainModelToTrainController.sendCurrStation.emit(trainObject.calculations["trainID"], trainObject.calculations["currStation"])
            trainModelToTrainController.sendLeftDoor.emit(trainObject.calculations["trainID"], trainObject.passenger_status["left_door"])
            trainModelToTrainController.sendRightDoor.emit(trainObject.calculations["trainID"], trainObject.passenger_status["right_door"])
            trainModelToTrainController.sendBlockNumber.emit(trainObject.calculations["trainID"], trainObject.calculations["currBlock"])            
            if trainObject.calculations["initialized"]:
                trainModelToTrackModel.sendPolarity.emit(trainObject.calculations["line"], trainObject.calculations["currBlock"], trainObject.calculations["prevBlock"])
                trainObject.calculations["initialized"] = False
            if trainObject.calculations["distance"] == trainObject.navigation_status["block_length"]:
                trainObject.calculations["distance"] = 0
                trainObject.calculations["polarity"] = not trainObject.calculations["polarity"]
                trainModelToTrackModel.sendPolarity.emit(trainObject.calculations["line"], trainObject.calculations["currBlock"], trainObject.calculations["prevBlock"])
            trainModelToTrainController.sendPolarity.emit(trainObject.calculations["trainID"], trainObject.calculations["polarity"])
            # trainObject.calculations["currBlock"] = trainObject.calculations["nextBlock"]
            trainObject.calculations["prevBlock"] = trainObject.calculations["currBlock"]

    def signal_blockInfo(self, nextBlock, blockLength, blockGrade, speedLimit, suggestedSpeed, authority):
        for trainObject in self.trainsList:
            trainObject.calculations["nextBlock"] = nextBlock
            trainObject.navigation_status["block_length"] = blockLength
            trainObject.navigation_status["block_grade"] = blockGrade
            trainObject.vehicle_status["speed_limit"] = speedLimit
            trainObject.vehicle_status["commanded_speed"] = suggestedSpeed
            trainObject.navigation_status["authority"] = authority
        return

    def signal_beacon(self, beaconDict):
        for trainObject in self.trainsList:
            if trainObject.calulations["currStation"] == trainObject.navigation_status["next_station"]:
                trainObject.navigation_status["prev_station"] = trainObject.calulations["currStation"]
                trainModelToTrackModel.sendCurrentPassengers.emit(trainObject.calculations["line"], trainObject.calculations["currStation"], trainObject.passenger_status["passengers"])
            
            trainObject.calculations["nextStation1"] = beaconDict["Next Station1"]
            trainObject.calculations["nextStation2"] = beaconDict["Next Station2"]
            trainObject.calculations["currStation"] = beaconDict["Current Station"]
            trainObject.calculations["doorSide"] = beaconDict["Door Side"]

            if trainObject.calculations["nextStation1"] == trainObject.navigation_status["prev_station"]:
                trainObject.navigation_status["next_station"] = trainObject.calculations["nextStation2"]
            else: 
                trainObject.navigation_status["next_station"] = trainObject.calculations["nextStation1"]
            
        return

    def signal_new_passengers(self, passengers):
        for trainObject in self.trainsList:
            trainObject.passenger_status["passengers"] = passengers
        return
    def signal_power(self, id, power):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.vehicle_status["power"] = power

    def signal_interior_lights(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["lights_status"] = status

    def signal_left_door(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["left_door"] = status

    def signal_right_door(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["right_door"] = status

    def signal_temperature(self, id, temp):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.calculations["setpoint_temp"] = temp

    def signal_advertisements(self, id, val):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["advertisements"] = val

    def signal_headlights(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.navigation_status["headlights"] = status

    def signal_brake(self, id, eff):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.vehicle_status["brakes"] = eff

    def signal_emergency_brake(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.failure_status["emergency_brake"] = status

    def signal_announcement(self, id, ann):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["announcements"] = ann

class ResultsWindow(QMainWindow):
    # Font variables
    textFontSize = 10
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = "Product Sans"

    # Color variables
    colorDarkBlue = "#085394"
    colorLightRed = "#EA9999"
    colorLightBlue = "#9FC5F8"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"
    colorBlack = "#000000"

    # Dimensions
    w = 960
    h = 960

    moduleName = "Results Window"

    def __init__(self, selected_text, trains):
        super().__init__()
        # Trains List
        self.trainsList = trains

        ############

        self.time_interval = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update
        )  # Connect the timer to the update_text function
        self.timer.start(
            self.time_interval
        )  # Update the text every 1000 milliseconds (1 second)

        self.sysTime = QDateTime.currentDateTime()
        self.sysTime.setTime(QTime(0, 0, 0))

        """ Header Template """

        # Setting title
        self.setWindowTitle(self.moduleName)

        # Setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        # Body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet(
            "background-color: white;" "border: 1px solid black"
        )

        # Header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet(
            "background-color:" + self.colorDarkBlue + ";" "border: 1px solid black"
        )

        # Title
        self.titleLabel = QLabel("Train Model", self)
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        title_width = 400
        title_height = 50
        title_x = (self.width() - title_width) // 2
        title_y = 35
        self.titleLabel.setGeometry(title_x, title_y, title_width, title_height)
        self.titleLabel.setStyleSheet("color: white")

        # MTA Logo
        self.pixmapMTALogo = QtGui.QPixmap("src/main/TrainModel/MTA_Logo.png")
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # Module
        self.moduleLabel = QLabel("Train Model", self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # Test bench icon
        self.pixmapGear = QtGui.QPixmap("src/main/TrainModel/gear_icon.png")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # Test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # System time input
        self.systemTimeInput = QLabel("00:00:00", self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet("color:" + self.colorDarkBlue)

        # System time label
        self.systemTimeLabel = QLabel("System Time:", self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed label
        self.systemSpeedLabel = QLabel("System Speed:", self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(689, 140, 100, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed input
        self.systemSpeedInput = QLabel("x1.0", self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)

        # Increase system speed button
        self.pixmapFastForward = QtGui.QPixmap("src/main/TrainModel/fast-forward.svg")
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 143, 20, 20)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # Decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("src/main/TrainModel/rewind.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(819, 143, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # Create a QLabel to display the drop-down text
        current_train = QLabel(self)
        current_train.setText(f"Selected Train: {selected_text}")
        current_train.setFont(QFont(self.fontStyle, 16))
        current_train.setGeometry(QRect(275, 100, 400, 50))
        current_train.setAlignment(Qt.AlignCenter)

        # Extract the selected train name from the QLabel's text
        self.selected_train_name = current_train.text().split(":")[-1].strip()

        """ Vehicle Status """

        # Create a QLabel for the vehicle status window
        self.vehicle_label = QLabel(self.bodyBlock)
        self.vehicle_label.setGeometry(QRect(75, 170, 350, 300))
        self.vehicle_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for vehicle status
        self.vehicle_background_widget = QWidget(self.vehicle_label)
        self.vehicle_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.vehicle_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white backgrounds for vehicle status
        self.vehicle_background_layout = QVBoxLayout(self.vehicle_background_widget)
        self.vehicle_background_layout.setContentsMargins(0, 0, 0, 0)
        self.vehicle_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue for vehicle status
        self.vehicle_white_background_label = QLabel(self.bodyBlock)
        self.vehicle_white_background_label.setGeometry(QRect(75, 200, 350, 300))
        self.vehicle_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for vehicle status
        self.vehicle_white_background_layout = QVBoxLayout(
            self.vehicle_white_background_label
        )
        self.vehicle_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.vehicle_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        self.vehicle_word_list = [
            "Speed Limit: {} mph",
            "Current Speed: {} mph",
            "Setpoint Speed: {} mph",
            "Commanded Speed: {} mph",
            "Acceleration: {} ft/s",
            "Brakes: {}",
            "Power: {} kW",
            "Power Limit: {} kW",
        ]

        # QLabel for speed limit
        self.word_label_speed_limit = QLabel(
            "Speed Limit: {} mph".format(self.trainsList[0].vehicle_status["speed_limit"]),
            self.vehicle_white_background_label
        )
        self.word_label_speed_limit.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_speed_limit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_speed_limit.setContentsMargins(5, 5, 5, 5)
        self.word_label_speed_limit.setFont(QFont("Arial", 9))

        # QLabel for current speed
        self.word_label_current_speed = QLabel(
            "Current Speed: {} mph".format(self.trainsList[0].vehicle_status["current_speed"]),
            self.vehicle_white_background_label
        )
        self.word_label_current_speed.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_current_speed.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_current_speed.setContentsMargins(5, 5, 5, 5)
        self.word_label_current_speed.setFont(QFont("Arial", 9))

        # QLabel for Setpoint Speed
        self.word_label_setpoint_speed = QLabel(
            "Setpoint Speed: {} mph".format(self.trainsList[0].vehicle_status["setpoint_speed"]),
            self.vehicle_white_background_label
        )
        self.word_label_setpoint_speed.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_setpoint_speed.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_setpoint_speed.setContentsMargins(5, 5, 5, 5)
        self.word_label_setpoint_speed.setFont(QFont("Arial", 9))

        # QLabel for commanded speed
        self.word_label_commanded_speed = QLabel(
            "Commanded Speed: {} mph".format(self.trainsList[0].vehicle_status["commanded_speed"]),
            self.vehicle_white_background_label
        )
        self.word_label_commanded_speed.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_commanded_speed.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_commanded_speed.setContentsMargins(5, 5, 5, 5)
        self.word_label_commanded_speed.setFont(QFont("Arial", 9))

        # QLabel for acceleration
        self.word_label_acceleration = QLabel(
            "Acceleration: {} ft/s".format(self.trainsList[0].vehicle_status["acceleration"]),
            self.vehicle_white_background_label
        )
        self.word_label_acceleration.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_acceleration.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_acceleration.setContentsMargins(5, 5, 5, 5)
        self.word_label_acceleration.setFont(QFont("Arial", 9))

        # QLabel for brakes
        self.word_label_brakes = QLabel(
            "Brakes: {}".format(self.trainsList[0].vehicle_status["brakes"]),
            self.vehicle_white_background_label
        )
        self.word_label_brakes.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_brakes.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_brakes.setContentsMargins(5, 5, 5, 5)
        self.word_label_brakes.setFont(QFont("Arial", 9))

        # QLabel for power
        self.word_label_power = QLabel(
            "Power: {} kW".format(self.trainsList[0].vehicle_status["power"]),
            self.vehicle_white_background_label
        )
        self.word_label_power.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_power.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_power.setContentsMargins(5, 5, 5, 5)
        self.word_label_power.setFont(QFont("Arial", 9))

        # QLabel for power limit
        self.word_label_power_limit = QLabel(
            "Power Limit: {} kW".format(self.trainsList[0].vehicle_status["power_limit"]),
            self.vehicle_white_background_label
        )
        self.word_label_power_limit.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_power_limit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_power_limit.setContentsMargins(5, 5, 5, 5)
        self.word_label_power_limit.setFont(QFont("Arial", 9))

        # Add QLabel widgets to layout
        self.vehicle_white_background_layout.addWidget(
            self.word_label_speed_limit, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_current_speed, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_setpoint_speed, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_commanded_speed, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_acceleration, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_brakes, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_power, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_power_limit, alignment=Qt.AlignTop
        )

        # Add stretch
        self.vehicle_white_background_layout.addStretch(1)
        
        # self.vehicle_status = {}
        # self.vehicle_labels = []

        # # Check if the selected train exists in the trains dictionary
        # if self.selected_train_name in self.trains.trains:
        #     train_data = self.trains.trains[self.selected_train_name]
        #     self.vehicle_status = train_data.get("vehicle_status", {})

        #     # Create and add QLabel widgets for each word the layout in vehicle status
        #     for word_placeholders in self.vehicle_word_list:
        #         word_key = (
        #             word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
        #         )
        #         word_value = self.vehicle_status.get(word_key, "N/A")

        #         # Create the QLabel widget
        #         if (
        #             "{}" in word_placeholders
        #             and "{}" in word_placeholders[word_placeholders.find("{}") + 2 :]
        #         ):  # Check if there are two placeholders in the string
        #             word = word_placeholders.format(
        #                 self.selected_train_name, word_value
        #             )
        #         else:
        #             word = word_placeholders.format(word_value)

        #         # Create the QLabel widget
        #         self.word_label = QLabel(word, self.vehicle_white_background_label)
        #         self.word_label.setStyleSheet(
        #             "color: #000000; background-color: transparent; border: none;"
        #         )
        #         self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         self.word_label.setContentsMargins(5, 5, 5, 5)
        #         self.word_label.setFont(QFont("Arial", 9))

        #         self.vehicle_labels.append(self.word_label)

        #         self.vehicle_white_background_layout.addWidget(
        #             self.word_label, alignment=Qt.AlignTop
        #         )

        # self.vehicle_white_background_layout.addStretch(1)

        # Create the title label for vehicle status
        self.vehicle_title_label = QLabel("Vehicle Status:", self.vehicle_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.vehicle_title_label.setFont(self.font)
        self.vehicle_title_label.setStyleSheet(
            "color: #FFFFFF; background-color: transparent; border: none;"
        )
        self.vehicle_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.vehicle_title_label.setGeometry(
            QRect(
                0,
                0,
                self.vehicle_background_widget.width(),
                self.vehicle_background_widget.height(),
            )
        )

        """ Failure Status """

        # Create a QLabel for the failure rectangle
        self.failure_label = QLabel(self.bodyBlock)
        self.failure_label.setGeometry(QRect(500, 170, 350, 300))
        self.failure_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the red and white backgrounds for failure window
        self.failure_background_widget = QWidget(self.failure_label)
        self.failure_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.failure_background_widget.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget for failure window
        self.failure_white_background_layout = QVBoxLayout(
            self.failure_background_widget
        )
        self.failure_white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.failure_white_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the red for failure window
        self.failure_white_background_label = QLabel(self.bodyBlock)
        self.failure_white_background_label.setGeometry(QRect(500, 200, 350, 300))
        self.failure_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header for failure window
        self.failure_white_background_layout = QVBoxLayout(
            self.failure_white_background_label
        )
        self.failure_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.failure_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        failure_word_list = [
            "Engine Failure: {}",
            "Signal Pickup Failure: {}",
            "Brake Failure: {}",
            "Emergency Brake: {}",
        ]

        # QLabel for engine failure
        self.word_label_engine_failure = QLabel(
            "Engine Failure: {}".format(self.trainsList[0].failure_status["engine_failure"]),
            self.failure_white_background_label
        )
        self.word_label_engine_failure.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_engine_failure.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_engine_failure.setContentsMargins(0, 0, 0, 0)
        self.word_label_engine_failure.setFont(QFont("Arial", 9))

        # QLabel for signal pickup failure
        self.word_label_signal_pickup_failure = QLabel(
            "Signal Pickup Failure: {}".format(self.trainsList[0].failure_status["signal_pickup_failure"]),
            self.failure_white_background_label
        )
        self.word_label_signal_pickup_failure.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_signal_pickup_failure.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_signal_pickup_failure.setContentsMargins(0, 0, 0, 0)
        self.word_label_signal_pickup_failure.setFont(QFont("Arial", 9))

        # QLabel for brake failure
        self.word_label_brake_failure = QLabel(
            "Brake Failure: {}".format(self.trainsList[0].failure_status["brake_failure"]),
            self.failure_white_background_label
        )
        self.word_label_brake_failure.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_brake_failure.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_brake_failure.setContentsMargins(0, 0, 0, 0)
        self.word_label_brake_failure.setFont(QFont("Arial", 9))

        # QLabel for emergency brake
        self.word_label_emergency_brake = QLabel(
            "Emergency Brake: {}".format(self.trainsList[0].failure_status["emergency_brake"]),
            self.failure_white_background_label
        )
        self.word_label_emergency_brake.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_emergency_brake.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_emergency_brake.setContentsMargins(0, 0, 0, 0)
        self.word_label_emergency_brake.setFont(QFont("Arial", 9))

        # Add QLabel widgets to layout
        self.failure_white_background_layout.addWidget(
            self.word_label_engine_failure, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.failure_white_background_layout.addWidget(
            self.word_label_signal_pickup_failure, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.failure_white_background_layout.addWidget(
            self.word_label_brake_failure, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.failure_white_background_layout.addWidget(
            self.word_label_emergency_brake, alignment=Qt.AlignTop
        )
        
        # failure_status = {}

        # # Check if the selected train exists in the trains dictionary
        # if self.selected_train_name in self.trains.trains:
        #     train_data = self.trains.trains[self.selected_train_name]
        #     failure_status = train_data.get("failure_status", {})

        #     # Iterate through the failure_word_list
        #     for word_placeholders in failure_word_list:
        #         word_key = (
        #             word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
        #         )

        #         # Create the QLabel widget for failure name
        #         failure_label_text = word_placeholders.format("")
        #         failure_label = QLabel(
        #             failure_label_text, self.failure_white_background_label
        #         )
        #         failure_label.setStyleSheet(
        #             "color: #000000; background-color: transparent; border: none;"
        #         )
        #         failure_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         failure_label.setContentsMargins(10, 10, 10, 10)
        #         failure_label.setFont(QFont("Arial", 9))

        #         # Create the QCheckBox widget
        #         check = QCheckBox()

        #         # Set the checkbox state based on the value in failure_status
        #         check.setChecked(
        #             self.trains.get_value(
        #                 self.selected_train_name, "failure_status", word_key
        #             )
        #         )

        #         # Create a QHBoxLayout for each failure and add QLabel and QCheckBox to it
        #         failure_layout = QHBoxLayout()
        #         failure_layout.addWidget(failure_label)
        #         failure_layout.addWidget(check)
        #         failure_layout.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        #         failure_layout.setContentsMargins(10, 10, 10, 10)

        #         # Add the QHBoxLayout to the main layout
        #         self.failure_white_background_layout.addLayout(failure_layout)

        #         # Connect the checkbox state change to a function/slot
        #         check.stateChanged.connect(
        #             lambda state, train=self.selected_train_name, key=word_key, checkbox=check: self.update_failure_status(
        #                 train, key, checkbox.isChecked()
        #             )
        #         )

        # self.failure_white_background_layout.addStretch(1)

        # Create the title label
        self.failure_title_label = QLabel("Failures:", self.failure_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.failure_title_label.setFont(self.font)
        self.failure_title_label.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.failure_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.failure_title_label.setGeometry(
            QRect(
                0,
                0,
                self.failure_background_widget.width(),
                self.failure_background_widget.height(),
            )
        )

        """ Passenger Status """

        # Create a QLabel for the Passenger Status
        self.passenger_label = QLabel(self.bodyBlock)
        self.passenger_label.setGeometry(QRect(75, 550, 350, 300))
        self.passenger_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for passenger status
        self.passenger_background_widget = QWidget(self.passenger_label)
        self.passenger_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.passenger_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget for passenger status
        self.passenger_background_layout = QVBoxLayout(self.passenger_background_widget)
        self.passenger_background_layout.setContentsMargins(0, 0, 0, 0)
        self.passenger_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.passenger_white_background_label = QLabel(self.bodyBlock)
        self.passenger_white_background_label.setGeometry(QRect(75, 580, 350, 300))
        self.passenger_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for vehicle status
        self.passenger_white_background_layout = QVBoxLayout(
            self.passenger_white_background_label
        )
        self.passenger_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.passenger_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        self.passenger_word_list = [
            "Passengers: {}",
            "Passenger Limit: {}",
            "Left Door: {}",
            "Right Door: {}",
            "Lights Status: {}",
            "Announcements: {}",
            "Temperature: {}",
            "Air Conditioning: {}",
            "Advertisements: {}",
        ]

        # QLabel for passengers
        self.word_label_passengers = QLabel(
            "Passengers: {}".format(self.trainsList[0].passenger_status["passengers"]),
            self.passenger_white_background_label
            
        )
        self.word_label_passengers.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_passengers.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_passengers.setContentsMargins(5, 5, 5, 5)
        self.word_label_passengers.setFont(QFont("Arial", 9))

        # QLabel for passenger limit
        self.word_label_passenger_limit = QLabel(
            "Passenger Limit: {}".format(self.trainsList[0].passenger_status["passenger_limit"]),
            self.passenger_white_background_label
        )
        self.word_label_passenger_limit.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_passenger_limit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_passenger_limit.setContentsMargins(5, 5, 5, 5)
        self.word_label_passenger_limit.setFont(QFont("Arial", 9))

        # QLabel for left door
        self.word_label_left_door = QLabel(
            "Left Door: {}".format(self.trainsList[0].passenger_status["left_door"]),
            self.passenger_white_background_label
        )
        self.word_label_left_door.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_left_door.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_left_door.setContentsMargins(5, 5, 5, 5)
        self.word_label_left_door.setFont(QFont("Arial", 9))

        # QLabel for right door
        self.word_label_right_door = QLabel(
            "Right Door: {}".format(self.trainsList[0].passenger_status["right_door"]),
            self.passenger_white_background_label
        )
        self.word_label_right_door.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_right_door.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_right_door.setContentsMargins(5, 5, 5, 5)
        self.word_label_right_door.setFont(QFont("Arial", 9))

        # QLabel for lights status
        self.word_label_lights_status = QLabel(
            "Lights Status: {}".format(self.trainsList[0].passenger_status["lights_status"]),
            self.passenger_white_background_label
        )
        self.word_label_lights_status.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_lights_status.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_lights_status.setContentsMargins(5, 5, 5, 5)
        self.word_label_lights_status.setFont(QFont("Arial", 9))

        # QLabel for announcements
        self.word_label_announcements = QLabel(
            "Announcements: {}".format(self.trainsList[0].passenger_status["announcements"]),
            self.passenger_white_background_label
        )
        self.word_label_announcements.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_announcements.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_announcements.setContentsMargins(5, 5, 5, 5)
        self.word_label_announcements.setFont(QFont("Arial", 9))

        # QLabel for temperature
        self.word_label_temperature = QLabel(
            "Temperature: {}".format(self.trainsList[0].passenger_status["temperature"]),
            self.passenger_white_background_label
        )
        self.word_label_temperature.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_temperature.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_temperature.setContentsMargins(5, 5, 5, 5)
        self.word_label_temperature.setFont(QFont("Arial", 9))

        # QLabel for air conditioning
        self.word_label_air_conditioning = QLabel(
            "Air Conditioning: {}".format(self.trainsList[0].passenger_status["air_conditioning"]),
            self.passenger_white_background_label
        )
        self.word_label_air_conditioning.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_air_conditioning.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_air_conditioning.setContentsMargins(5, 5, 5, 5)
        self.word_label_air_conditioning.setFont(QFont("Arial", 9))

        # QLabel for advertisements
        self.word_label_advertisements = QLabel(
            "Advertisements: {}".format(self.trainsList[0].passenger_status["advertisements"]),
            self.passenger_white_background_label
        )
        self.word_label_advertisements.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_advertisements.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_advertisements.setContentsMargins(5, 5, 5, 5)
        self.word_label_advertisements.setFont(QFont("Arial", 9))

        # Add QLabel widgets to layout
        self.passenger_white_background_layout.addWidget(
            self.word_label_passengers, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_passenger_limit, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_left_door, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_right_door, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_lights_status, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_announcements, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_temperature, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_air_conditioning, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_advertisements, alignment=Qt.AlignTop
        )

        # Add stretch
        self.passenger_white_background_layout.addStretch(1)
        
        # self.passenger_status = {}
        # self.passenger_labels = []

        # # Check if the selected train exists in the trains dictionary
        # if self.selected_train_name in self.trains.trains:
        #     train_data = self.trains.trains[self.selected_train_name]
        #     self.passenger_status = train_data.get("passenger_status", {})

        #     # Create and add QLabel widgets for each word in the layout in passenger status
        #     for word_placeholders in self.passenger_word_list:
        #         word_key = (
        #             word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
        #         )
        #         word_value = self.passenger_status.get(word_key, "N/A")

        #         # Create the QLabel widget
        #         if (
        #             "{}" in word_placeholders
        #             and "{}" in word_placeholders[word_placeholders.find("{}") + 2 :]
        #         ):
        #             word = word_placeholders.format(
        #                 self.selected_train_name, word_value
        #             )
        #         else:
        #             word = word_placeholders.format(word_value)

        #         self.word_label = QLabel(word, self.passenger_white_background_label)
        #         self.word_label.setStyleSheet(
        #             "color: #000000; background-color: transparent; border: none;"
        #         )
        #         self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         self.word_label.setContentsMargins(5, 5, 5, 5)
        #         self.word_label.setFont(QFont("Arial", 9))

        #         self.passenger_labels.append(self.word_label)

        #         self.passenger_white_background_layout.addWidget(
        #             self.word_label, alignment=Qt.AlignTop
        #         )

        # self.passenger_white_background_layout.addStretch(1)

        # Create the title label
        self.passenger_title_label = QLabel("Passenger Status:", self.passenger_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.passenger_title_label.setFont(self.font)
        self.passenger_title_label.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.passenger_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.passenger_title_label.setGeometry(
            QRect(
                0,
                0,
                self.passenger_background_widget.width(),
                self.passenger_background_widget.height(),
            )
        )

        """ Navigation Status """

        # Create a QLabel for the Navigation status
        self.navigation_label = QLabel(self.bodyBlock)
        self.navigation_label.setGeometry(QRect(500, 550, 350, 300))
        self.navigation_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for navigation status
        self.navigation_background_widget = QWidget(self.navigation_label)
        self.navigation_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.navigation_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget for navigation status
        self.navigation_background_layout = QVBoxLayout(
            self.navigation_background_widget
        )
        self.navigation_background_layout.setContentsMargins(0, 0, 0, 0)
        self.navigation_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue for navigation status
        self.navigation_white_background_label = QLabel(self.bodyBlock)
        self.navigation_white_background_label.setGeometry(QRect(500, 580, 350, 300))
        self.navigation_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for navigation status
        self.navigation_white_background_layout = QVBoxLayout(
            self.navigation_white_background_label
        )
        self.navigation_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.navigation_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        self.navigation_word_list = [
            "Authority: {}",
            "Beacon: {}",
            "Block Length: {}",
            "Block Grade: {}",
            "Next Station: {}",
            "Previous Station: {}",
            "Headlights: {}",
            "Passenger Emergency Brake: {}",
        ]

        # QLabel for authority
        self.word_label_authority = QLabel(
            "Authority: {}".format(self.trainsList[0].navigation_status["authority"]),
            self.navigation_white_background_label
        )
        self.word_label_authority.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_authority.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_authority.setContentsMargins(5, 5, 5, 5)
        self.word_label_authority.setFont(QFont("Arial", 9))

        # QLabel for beacon
        self.word_label_beacon = QLabel(
            "Beacon: {}".format(self.trainsList[0].navigation_status["beacon"]),
            self.navigation_white_background_label
        )
        self.word_label_beacon.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_beacon.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_beacon.setContentsMargins(5, 5, 5, 5)
        self.word_label_beacon.setFont(QFont("Arial", 9))

        # QLabel for block length
        self.word_label_block_length = QLabel(
            "Block Length: {}".format(self.trainsList[0].navigation_status["block_length"]),
            self.navigation_white_background_label
        )
        self.word_label_block_length.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_block_length.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_block_length.setContentsMargins(5, 5, 5, 5)
        self.word_label_block_length.setFont(QFont("Arial", 9))

        # QLabel for block grade
        self.word_label_block_grade = QLabel(
            "Block Grade: {}".format(self.trainsList[0].navigation_status["block_grade"]),
            self.navigation_white_background_label
        )
        self.word_label_block_grade.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_block_grade.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_block_grade.setContentsMargins(5, 5, 5, 5)
        self.word_label_block_grade.setFont(QFont("Arial", 9))

        # QLabel for next station
        self.word_label_next_station = QLabel(
            "Next Station: {}".format(self.trainsList[0].navigation_status["next_station"]),
            self.navigation_white_background_label
        )
        self.word_label_next_station.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_next_station.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_next_station.setContentsMargins(5, 5, 5, 5)
        self.word_label_next_station.setFont(QFont("Arial", 9))

        # QLabel for prev station
        self.word_label_prev_station = QLabel(
            "Previous Station: {}".format(self.trainsList[0].navigation_status["prev_station"]),
            self.navigation_white_background_label
        )
        self.word_label_prev_station.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_prev_station.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_prev_station.setContentsMargins(5, 5, 5, 5)
        self.word_label_prev_station.setFont(QFont("Arial", 9))

        # QLabel for headlights
        self.word_label_headlights = QLabel(
            "Headlights: {}".format(self.trainsList[0].navigation_status["headlights"]),
            self.navigation_white_background_label
        )
        self.word_label_headlights.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_headlights.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_headlights.setContentsMargins(5, 5, 5, 5)
        self.word_label_headlights.setFont(QFont("Arial", 9))

        # QLabel for passenger emergency brake
        self.word_label_pass_emergency_brake = QLabel(
            "Passenger Emergency Brake: {}".format(self.trainsList[0].navigation_status["passenger_emergency_brake"]),
            self.navigation_white_background_label
        )
        self.word_label_pass_emergency_brake.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_pass_emergency_brake.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_pass_emergency_brake.setContentsMargins(5, 5, 5, 5)
        self.word_label_pass_emergency_brake.setFont(QFont("Arial", 9))

        # Add QLabel widgets to layout
        self.navigation_white_background_layout.addWidget(
            self.word_label_authority, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_beacon, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_block_length, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_block_grade, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_next_station, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_prev_station, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_headlights, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_pass_emergency_brake, alignment=Qt.AlignTop
        )

        # Add stretch
        self.navigation_white_background_layout.addStretch(1)
        
        # self.navigation_status = {}
        # self.navigation_labels = []

        # # Check if the selected train exists in the trains dictionary
        # if self.selected_train_name in self.trains.trains:
        #     train_data = self.trains.trains[self.selected_train_name]
        #     navigation_status = train_data.get("navigation_status", {})

        #     # Create and add QLabel widgets for each word the layout in navigation status
        #     for word_placeholders in self.navigation_word_list:
        #         word_key = (
        #             word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
        #         )
        #         word_value = navigation_status.get(word_key, "N/A")

        #         # Create the QLabel widget
        #         if (
        #             "{}" in word_placeholders
        #             and "{}" in word_placeholders[word_placeholders.find("{}") + 2 :]
        #         ):
        #             word = word_placeholders.format(
        #                 self.selected_train_name, word_value
        #             )
        #         else:
        #             word = word_placeholders.format(word_value)

        #         self.word_label = QLabel(word, self.navigation_white_background_label)
        #         self.word_label.setStyleSheet(
        #             "color: #000000; background-color: transparent; border: none;"
        #         )
        #         self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         self.word_label.setContentsMargins(5, 5, 5, 5)
        #         self.word_label.setFont(QFont("Arial", 9))

        #         self.navigation_labels.append(self.word_label)

        #         self.navigation_white_background_layout.addWidget(
        #             self.word_label, alignment=Qt.AlignTop
        #         )

        # self.navigation_white_background_layout.addStretch(1)

        # Create the title label
        self.navigation_title_label = QLabel(
            "Navigation Status:", self.navigation_label
        )
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.navigation_title_label.setFont(self.font)
        self.navigation_title_label.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.navigation_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.navigation_title_label.setGeometry(
            QRect(
                0,
                0,
                self.navigation_background_widget.width(),
                self.navigation_background_widget.height(),
            )
        )

    def update_failure_status(self, train_name, key, state):
        # Sets the value of the dictionary value for the failure variables
        self.trains.set_value(train_name, "failure_status", key, state)

    def update_ui(self):
        word_value = {}
        if self.vehicle_word_list:
            # Update each UI element with the corresponding variable from the SharedData dictionary class
            for i, word_placeholders in enumerate(self.vehicle_word_list):
                word_key = (
                    word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
                )

                label_text = word_placeholders.format(word_value)

                # Update the text of the QLabel
                self.vehicle_labels[i].setText(label_text)

        if self.passenger_word_list:
            for i, word_placeholders in enumerate(self.passenger_word_list):
                word_key = (
                    word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
                )

                label_text = word_placeholders.format(word_value)

                # Update the text of the QLabel
                self.passenger_labels[i].setText(label_text)

        if self.navigation_word_list:
            for i, word_placeholders in enumerate(self.navigation_word_list):
                word_key = (
                    word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
                )

                label_text = word_placeholders.format(word_value)

                # Update the text of the QLabel
                self.navigation_labels[i].setText(label_text)

    def signal_period(self, period):
        self.time_interval = period

    def update(self):
        # system time
        # self.sysTime = self.sysTime.addSecs(1)
        masterSignals.timingMultiplier.connect(self.signal_period)
        masterSignals.clockSignal.connect(self.sysTime.setTime)

        self.timer.setInterval(self.time_interval)

        self.systemTimeInput.setText(self.sysTime.toString("HH:mm:ss"))
        self.systemSpeedInput.setText(
            "x" + format(1 / (self.time_interval / 1000), ".3f")
        )

        for trainObject in self.trainsList:
            # Update QLabel widgets with new information
            self.word_label_speed_limit.setText(
                "Speed Limit: {} mph".format(trainObject.vehicle_status["speed_limit"])
            )

            self.word_label_current_speed.setText(
                "Current Speed: {} mph".format(trainObject.vehicle_status["current_speed"])
            )

            self.word_label_setpoint_speed.setText(
                "Setpoint Speed: {} mph".format(trainObject.vehicle_status["setpoint_speed"])
            )

            self.word_label_commanded_speed.setText(
                "Commanded Speed: {} mph".format(trainObject.vehicle_status["commanded_speed"])
            )
            
            self.word_label_acceleration.setText(
                "Acceleration: {} ft/s".format(trainObject.vehicle_status["acceleration"])
            )

            self.word_label_brakes.setText(
                "Brakes: {}".format(trainObject.vehicle_status["brakes"])
            )
            
            self.word_label_power.setText(
                "Power: {} kW".format(trainObject.vehicle_status["power"])
            )

            self.word_label_power_limit.setText(
                "Power Limit: {} kW".format(trainObject.vehicle_status["power_limit"])
            )

            self.word_label_engine_failure.setText(
                "Engine Failure: {}".format(self.trainsList[0].failure_status["engine_failure"])
            )

            self.word_label_signal_pickup_failure.setText(
                "Signal Pickup Failure: {}".format(self.trainsList[0].failure_status["signal_pickup_failure"])
            )

            self.word_label_brake_failure.setText(
                "Brake Failure: {}".format(self.trainsList[0].failure_status["brake_failure"])
            )

            self.word_label_emergency_brake.setText(
                "Emergency Brake: {}".format(self.trainsList[0].failure_status["emergency_brake"])
            )

            self.word_label_passengers.setText(
                "Power Limit: {} kW".format(trainObject.vehicle_status["power_limit"])
            )

            self.word_label_power_limit.setText(
                "Passenger Limit: {}".format(trainObject.passenger_status["passenger_limit"])
            )

            self.word_label_left_door.setText(
                "Left Door: {}".format(trainObject.passenger_status["left_door"])
            )

            self.word_label_right_door.setText(
                "Right Door: {}".format(trainObject.passenger_status["right_door"])
            )

            self.word_label_lights_status.setText(
                "Lights Status: {}".format(trainObject.passenger_status["lights_status"])
            )

            self.word_label_announcements.setText(
                "Announcements: {}".format(trainObject.passenger_status["announcements"])
            )

            self.word_label_temperature.setText(
                "Temperature: {}".format(trainObject.passenger_status["temperature"])
            )

            self.word_label_air_conditioning.setText(
                "Air Conditioning: {}".format(trainObject.passenger_status["air_conditioning"])
            )

            self.word_label_advertisements.setText(
                "Advertisements: {}".format(trainObject.passenger_status["advertisements"])
            )

            self.word_label_authority.setText(
                "Authority: {}".format(trainObject.navigation_status["authority"])
            )

            self.word_label_beacon.setText(
                "Beacon: {}".format(trainObject.navigation_status["beacon"])
            )

            self.word_label_block_length.setText(
                "Block Length: {}".format(trainObject.navigation_status["block_length"])
            )

            self.word_label_block_grade.setText(
                "Block Grade: {}".format(trainObject.navigation_status["block_grade"])
            )

            self.word_label_next_station.setText(
                "Next Station: {}".format(trainObject.navigation_status["next_station"])
            )

            self.word_label_prev_station.setText(
                "Previous Station: {}".format(trainObject.navigation_status["prev_station"])
            )

            self.word_label_headlights.setText(
                "Headlights: {}".format(trainObject.navigation_status["headlights"])
            )

            self.word_label_pass_emergency_brake.setText(
                "Passenger Emergency Brake: {}".format(trainObject.navigation_status["passenger_emergency_brake"])
            )


# class SharedData:
#     def __init__(self):
#         self.trains = {
#             "Train 1": {
#                 "vehicle_status": {
#                     "speed_limit": 0,  # 1
#                     "current_speed": 0,  # 2
#                     "setpoint_speed": 0,  # 3
#                     "commanded_speed": 0,  # 4
#                     "acceleration": 0,  # 5
#                     "deceleration": 0,  # 6
#                     "brakes": False,  # 7
#                     "power": 0,  # 8
#                     "power_limit": 0,  # 9
#                 },
#                 "failure_status": {
#                     "engine_failure": False,  # 1
#                     "signal_pickup_failure": False,  # 2
#                     "brake_failure": False,  # 3
#                     "emergency_brake": False,  # 4
#                 },
#                 "passenger_status": {
#                     "passengers": 6,  # 1
#                     "passenger_limit": 74,  # 2
#                     "left_door": False,  # 3
#                     "right_door": False,  # 4
#                     "lights_status": False,  # 5
#                     "announcements": False,  # 6
#                     "temperature": 0,  # 7
#                     "air_conditioning": False,  # 8
#                     "advertisements": 0,  # 9
#                 },
#                 "navigation_status": {
#                     "authority": 0,  # 1
#                     "beacon": 0,  # 2
#                     "block_length": 0,  # 3
#                     "block_grade": 0,  # 4
#                     "next_station": "",  # 5
#                     "prev_station": "",  # 6
#                     "headlights": False,  # 7
#                     "passenger_emergency_brake": False,  # 8
#                 },
#                 "calculations": {
#                     "cars": 5,  # 1
#                     "mass": 5 * 56700,  # 2
#                     "length": 5 * 105.6,  # 3
#                     "currVelocity": 0,  # 4
#                     "currForce": 0,  # 5
#                     "currAcceleration": 0,  # 6
#                     "lastVelocity": 0,  # 7
#                     "lastAcceleration": 0,  # 8
#                     "lastPosition": 0,  # 9
#                     "nextBlock": 0,  # 10
#                     "currBlock": 0,  # 11
#                     "prevBlock": 0,  # 12
#                     "nextStation1": "",  # 13
#                     "nextStation2": "",  # 14
#                     "currStation": "",  # 15
#                     "line": "Green",  # 16
#                     "trainID": "",  # 17
#                 },
#             },
#         }
        # "Train 2": {
        #     "vehicle_status": {
        #         "speed_limit": 45,
        #         "current_speed": 45,
        #         "setpoint_speed": 55,
        #         "commanded_speed": 40,
        #         "acceleration": 3.5,
        #         "deceleration": 2.0,
        #         "brakes": True,
        #         "power": 75.0,
        #         "power_limit": 100.0,
        #     },
        #     "failure_status": {
        #         "engine_failure": False,
        #         "signal_pickup_failure": False,
        #         "brake_failure": False,
        #         "emergency_brake": False,
        #     },
        #     "passenger_status": {
        #         "passengers": 42,
        #         "passenger_limit": 50,
        #         "left_door": False,
        #         "right_door": True,
        #         "lights_status": True,
        #         "announcements": True,
        #         "temperature": 72,
        #         "air_conditioning": False,
        #         "advertisements": "Buy Drinks",
        #     },
        #     "navigation_status": {
        #         "authority": 5,
        #         "beacon": 6,
        #         "block_length": 2,
        #         "block_grade": 15,
        #         "next_station": 9,
        #         "prev_station": 5,
        #         "headlights": True,
        #         "passenger_emergency_brake": False,
        #     },
        # },
        # "Train 3": {
        #     "vehicle_status": {
        #         "speed_limit": 35,
        #         "current_speed": 45,
        #         "setpoint_speed": 55,
        #         "commanded_speed": 40,
        #         "acceleration": 3.5,
        #         "deceleration": 2.0,
        #         "brakes": True,
        #         "power": 75.0,
        #         "power_limit": 100.0,
        #     },
        #     "failure_status": {
        #         "engine_failure": False,
        #         "signal_pickup_failure": False,
        #         "brake_failure": False,
        #         "emergency_brake": False,
        #     },
        #     "passenger_status": {
        #         "passengers": 42,
        #         "passenger_limit": 50,
        #         "left_door": False,
        #         "right_door": True,
        #         "lights_status": True,
        #         "announcements": True,
        #         "temperature": 72,
        #         "air_conditioning": False,
        #         "advertisements": "Buy Drinks",
        #     },
        #     "navigation_status": {
        #         "authority": 5,
        #         "beacon": 6,
        #         "block_length": 2,
        #         "block_grade": 15,
        #         "next_station": 9,
        #         "prev_station": 5,
        #         "headlights": True,
        #         "passenger_emergency_brake": False,
        #     },
        # },
        # "Train 4": {
        #     "vehicle_status": {
        #         "speed_limit": 35,
        #         "current_speed": 45,
        #         "setpoint_speed": 55,
        #         "commanded_speed": 40,
        #         "acceleration": 3.5,
        #         "deceleration": 2.0,
        #         "brakes": True,
        #         "power": 75.0,
        #         "power_limit": 100.0,
        #     },
        #     "failure_status": {
        #         "engine_failure": False,
        #         "signal_pickup_failure": False,
        #         "brake_failure": False,
        #         "emergency_brake": False,
        #     },
        #     "passenger_status": {
        #         "passengers": 42,
        #         "passenger_limit": 50,
        #         "left_door": False,
        #         "right_door": True,
        #         "lights_status": True,
        #         "announcements": True,
        #         "temperature": 72,
        #         "air_conditioning": False,
        #         "advertisements": "Buy Drinks",
        #     },
        #     "navigation_status": {
        #         "authority": 5,
        #         "beacon": 6,
        #         "block_length": 2,
        #         "block_grade": 15,
        #         "next_station": 9,
        #         "prev_station": 5,
        #         "headlights": True,
        #         "passenger_emergency_brake": False,
        #     },
        # },
        # "Train 5": {
        #     "vehicle_status": {
        #         "speed_limit": 35,
        #         "current_speed": 45,
        #         "setpoint_speed": 55,
        #         "commanded_speed": 40,
        #         "acceleration": 3.5,
        #         "deceleration": 2.0,
        #         "brakes": True,
        #         "power": 75.0,
        #         "power_limit": 100.0,
        #     },
        #     "failure_status": {
        #         "engine_failure": False,
        #         "signal_pickup_failure": False,
        #         "brake_failure": False,
        #         "emergency_brake": False,
        #     },
        #     "passenger_status": {
        #         "passengers": 42,
        #         "passenger_limit": 50,
        #         "left_door": False,
        #         "right_door": True,
        #         "lights_status": True,
        #         "announcements": True,
        #         "temperature": 72,
        #         "air_conditioning": False,
        #         "advertisements": "Buy Drinks",
        #     },
        #     "navigation_status": {
        #         "authority": 5,
        #         "beacon": 6,
        #         "block_length": 2,
        #         "block_grade": 15,
        #         "next_station": 9,
        #         "prev_station": 5,
        #         "headlights": True,
        #         "passenger_emergency_brake": False,
        #     },

    # def get_value(self, train_name, category, key):
    #     return self.trains.get(train_name, {}).get(category, {}).get(key)

    # def set_value(self, train_name, category, key, value):
    #     if train_name in self.trains:
    #         if category in self.trains[train_name]:
    #             self.trains[train_name][category][key] = value


class TrainTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Train Model")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName("TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName("TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Train Model Test", self.central_widget)
        self.Title.setObjectName("Title")
        font = QFont()
        font.setFamilies(["Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(
            QCoreApplication.translate("TrainTest", "Train Model Test", None)
        )
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName("mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap("src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Train Image
        train_image_label = QLabel(self.central_widget)
        train_image_label.setObjectName("TrainImage")
        train_image_pixmap = QPixmap("src/main/TrainModel/Train_Image.jpg")
        max_image_height = 400  # You can change this to your desired height
        new_width = int(
            (train_image_pixmap.width() * max_image_height)
            / train_image_pixmap.height()
        )
        train_image_pixmap = train_image_pixmap.scaled(
            new_width, max_image_height, Qt.KeepAspectRatio
        )
        image_width = train_image_pixmap.width()
        image_height = train_image_pixmap.height()
        image_x = (self.width() - image_width) // 2
        image_y = 138 + 20
        train_image_label.setGeometry(
            QRect(image_x, image_y, image_width, image_height)
        )
        train_image_label.setPixmap(train_image_pixmap)
        train_image_label.setScaledContents(True)

        # Calculate the position for the Train Image
        image_width = train_image_pixmap.width()
        image_height = train_image_pixmap.height()
        image_x = (self.width() - image_width) // 2
        image_y = (138 + 0) + 20

        train_image_label.setGeometry(
            QRect(image_x, image_y, image_width, image_height)
        )

        # Search Bar
        search_bar_width = 500
        search_bar_height = 40
        search_bar_x = (self.width() - search_bar_width) // 2
        search_bar_y = image_y + image_height + 30  # Adjust the spacing as needed

        self.lineEdit = QLineEdit(self.central_widget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setGeometry(
            QRect(search_bar_x, search_bar_y, search_bar_width, search_bar_height)
        )
        font1 = QFont()
        font1.setPointSize(18)
        font1.setKerning(True)
        self.lineEdit.setFont(font1)

        # Push Buttons
        button_width = 150
        button_height = 50
        button_spacing = 30
        button_x = (self.width() - (3 * button_width + 2 * button_spacing)) // 2

        # First button
        self.pushButton = QPushButton(self.central_widget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(
            QRect(
                button_x,
                search_bar_y + search_bar_height + 10,
                button_width,
                button_height,
            )
        )
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setAutoRepeatInterval(105)

        # Second button
        self.pushButton_2 = QPushButton(self.central_widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setGeometry(
            QRect(
                button_x + button_width + button_spacing,
                search_bar_y + search_bar_height + 10,
                button_width,
                button_height,
            )
        )
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.setAutoRepeatInterval(105)

        # Third button
        self.pushButton_3 = QPushButton(self.central_widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setGeometry(
            QRect(
                button_x + 2 * (button_width + button_spacing),
                search_bar_y + search_bar_height + 10,
                button_width,
                button_height,
            )
        )
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setAutoRepeatInterval(105)

        self.setCentralWidget(self.central_widget)

        # Status Bar
        self.statusbar = self.statusBar()
        self.statusbar.setObjectName("statusbar")

        # Menu Bar
        self.menubar = self.menuBar()
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 720, 22))

        self.retranslateUi()

        # Track Model Test button press
        self.pushButton.setText(
            QCoreApplication.translate("TrainTest", "Track Model Test", None)
        )
        self.pushButton.clicked.connect(self.show_track_model_test)

        # Train Controller Test button press
        self.pushButton_2.setText(
            QCoreApplication.translate("TrainTest", "Train Controller Test", None)
        )
        self.pushButton_2.clicked.connect(self.show_train_controller_test)

        # Murphy button press
        self.pushButton_3.setText(
            QCoreApplication.translate("TrainTest", "Murphy Test", None)
        )
        self.pushButton_3.clicked.connect(self.show_murphy_test)

        # Create a "Main" button
        self.main_menu = QPushButton("Main", self.central_widget)
        self.main_menu.setObjectName("Main Menu")
        main_menu_width = 150
        main_menu_height = 65
        main_menu_x = self.width() - main_menu_width - 10
        main_menu_y = self.height() - main_menu_height - 30
        self.main_menu.setGeometry(
            QRect(main_menu_x, main_menu_y, main_menu_width, main_menu_height)
        )
        self.main_menu.setCursor(QCursor(Qt.PointingHandCursor))
        self.main_menu.setFont(QFont("Arial", 10))

        # Main button press
        self.main_menu.setText(
            QCoreApplication.translate("TrainTest", "Main Menu", None)
        )
        self.main_menu.clicked.connect(self.show_main_window)

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("TrainTest", "MainWindow", None))
        self.Title.setText(
            QCoreApplication.translate("TrainTest", "Train Model Test", None)
        )
        self.mtaLogo.setText("")
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(
            QCoreApplication.translate("TrainTest", "Train 1, 2, 3, 4", None)
        )
        self.pushButton.setText(
            QCoreApplication.translate("TrainTest", "Track Model Test", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate("TrainTest", "Train Controller Test", None)
        )
        self.pushButton_3.setText(
            QCoreApplication.translate("TrainTest", "Murphy Test", None)
        )

    def show_track_model_test(self):
        self.track_model_test = TrackModelTestWindow(self.clock)
        self.track_model_test.show()

    def show_train_controller_test(self):
        self.train_controller_test = TrainControllerTestWindow(self.clock)
        self.train_controller_test.show()

    def show_murphy_test(self):
        self.murphy_test = MurphyTestWindow(self.clock)
        self.murphy_test.show()

    def show_main_window(self):
        self.main_window = TrainModel()
        self.main_window.show()
        self.close()


class TrackModelTestWindow(QMainWindow):
    def __init__(self, clock):
        super().__init__()
        self.setWindowTitle("Track Model Test")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.clock = clock

        # Create a label for the clock in the main window
        self.font = QFont()
        self.font.setPointSize(20)
        self.clock_label = QLabel(self.central_widget)
        self.clock_label.setObjectName("clock_label")
        self.clock_label.setFont(self.font)
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Connect the clock's timeUpdated signal to the update_clock_label method
        self.clock.timeUpdated.connect(self.update_clock_label)

        # Start a timer to update the clock label periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock_label)
        self.timer.start(100)

        # Add the clock label to the central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.clock_label)
        self.layout.addStretch()

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName("TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName("TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Track Model Test", self.central_widget)
        self.Title.setObjectName("Title")
        font = QFont()
        font.setFamilies(["Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(
            QCoreApplication.translate("TrainTest", "Track Model Test", None)
        )
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName("mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap("src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Create a QLabel for the first rectangle
        self.rectangle_label = QLabel(self.central_widget)
        self.rectangle_label.setGeometry(QRect(50, 170, 590, 500))
        self.rectangle_label.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the blue and white backgrounds
        self.background_widget = QWidget(self.rectangle_label)
        self.background_widget.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget
        self.background_layout = QVBoxLayout(self.background_widget)
        self.background_layout.setContentsMargins(0, 0, 0, 0)
        self.background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.white_background_label = QLabel(self.central_widget)
        self.white_background_label.setGeometry(QRect(50, 210, 590, 430))
        self.white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header
        self.white_background_layout = QVBoxLayout(self.white_background_label)
        self.white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        word_list_1 = [
            "Speed Limit:",
            "Authority:",
            "Beacon:",
            "Passengers Entering:",
            "Acceleration Limit:",
            "Deceleration Limit:",
            "Brakes:",
            "Block Length:",
            "Direction of Travel:",
            "Block Elevation:",
        ]

        # Create and add QLineEdit widgets for the first word list
        self.value_inputs = {}
        for word_placeholder in word_list_1:
            word_label = QLabel(word_placeholder, self.white_background_label)
            word_label.setStyleSheet(
                "color: #000000; background-color: transparent; border: none;"
            )
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))

            value_input = QLineEdit(self.white_background_label)
            value_input.setStyleSheet(
                "background-color: #FFFFFF; border: 0.5px solid #000000;"
            )
            value_input.setContentsMargins(15, 15, 15, 15)

            word_layout = QHBoxLayout()
            word_layout.addWidget(word_label, alignment=Qt.AlignLeft)
            word_layout.addWidget(value_input, alignment=Qt.AlignLeft)

            self.white_background_layout.addLayout(word_layout)

            self.value_inputs[word_placeholder] = value_input

        self.white_background_layout.addStretch(1)

        # Create Apply and Reset buttons
        self.apply_button = QPushButton("Apply", self.central_widget)
        self.apply_button.setGeometry(1100, 640, 80, 30)
        self.apply_button.clicked.connect(self.apply_values)
        self.apply_button.setEnabled(True)

        self.reset_button = QPushButton("Reset", self.central_widget)
        self.reset_button.setGeometry(1190, 640, 80, 30)
        self.reset_button.clicked.connect(self.reset_values)
        self.reset_button.setEnabled(True)

        # Create the title label
        self.title_label = QLabel("Inputs:", self.rectangle_label)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator = QFrame(self.rectangle_label)
        self.line_separator.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator.setFrameShape(QFrame.HLine)
        self.line_separator.setFrameShadow(QFrame.Sunken)
        self.line_separator.setStyleSheet("background-color: #000000")

        # Create a QLabel for the second rectangle
        self.rectangle_label_2 = QLabel(self.central_widget)
        self.rectangle_label_2.setGeometry(QRect(640, 170, 590, 500))
        self.rectangle_label_2.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the red and white backgrounds
        self.background_widget_2 = QWidget(self.rectangle_label_2)
        self.background_widget_2.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget_2.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget
        self.white_background_layout_2 = QVBoxLayout(self.background_widget_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(0)

        # Create a QLabel for the white background below the red
        self.white_background_label_2 = QLabel(self.central_widget)
        self.white_background_label_2.setGeometry(QRect(640, 210, 590, 430))
        self.white_background_label_2.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header
        self.white_background_layout_2 = QVBoxLayout(self.white_background_label_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(5)

        # Create QLabel widgets for the list of words
        self.word_list_2 = [
            "Speed Limit:",
            "Authority:",
            "Commanded Speed:",
            "Current Speed:",
            "Temperature:",
            "Passengers Currently:",
            "Max Passengers:",
            "Next Station:",
            "Previous Station:",
            "Engine Failure:",
            "Signal Pickup Failure:",
            "Brake Failure:",
            "Power:",
            "Passenger Emergency Brake:",
        ]

        # Defines a dictionary with actual values for second set of words
        self.values_2 = {
            "Speed Limit:": "40 mph",
            "Authority:": "6 Blocks",
            "Commanded Speed:": "37 mph",
            "Current Speed:": "35 mph",
            "Temperature:": "78 ℉",
            "Passengers Currently:": "58",
            "Max Passengers:": "72",
            "Next Station:": "Block 7",
            "Previous Station:": "Block 3",
            "Engine Failure:": True,
            "Signal Pickup Failure:": False,
            "Brake Failure:": True,
            "Power:": "83 kW",
            "Passenger Emergency Brake:": "On",
        }

        # Initialize the list at the beginning of my method
        self.word_labels = []

        for word_placeholder in self.word_list_2:
            value = self.values_2.get(word_placeholder, "")
            label_text = f"{word_placeholder} {value}"
            word_label = QLabel(label_text, self.white_background_label_2)
            word_label.setStyleSheet(
                "color: #000000; background-color: transparent; border: none;"
            )
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))
            self.white_background_layout_2.addWidget(word_label, alignment=Qt.AlignTop)
            self.word_labels.append(word_label)

        # Create the title label
        self.title_label_2 = QLabel("Outputs:", self.rectangle_label_2)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label_2.setFont(self.font)
        self.title_label_2.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.title_label_2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label_2.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)
        self.line_separator_2.setStyleSheet("background-color: #000000")

    def apply_values(self):
        values_wordlist_1 = {}

        # Iterate through the input text boxes and update values_wordlist_1
        for word_placeholder, value_input in self.value_inputs.items():
            input_value = value_input.text()
            if input_value:
                try:
                    # Try to convert the input to an integer
                    input_value = int(input_value)
                except ValueError:
                    pass  # If it's not a valid integer, keep it as a string
                values_wordlist_1[word_placeholder] = input_value

        # Update the corresponding output values based on the mappings
        for word_placeholder, output_key in self.mapping.items():
            if word_placeholder in values_wordlist_1:
                self.values_2[output_key] = values_wordlist_1[word_placeholder]
                # Update the corresponding text box in the second set
                self.update_wordlist2_textbox(
                    output_key, values_wordlist_1[word_placeholder]
                )

        return values_wordlist_1

    def reset_values(self):
        default_values_wordlist_2 = {
            "Speed Limit": "45 mph",
            "Authority": "5 Blocks",
            "Commanded Speed": "35 mph",
            "Current Speed": "32 mph",
            "Temperature": "75 ℉",
            "Passengers Currently": "60",
            "Max Passengers": "74",
            "Next Station": "Block 9",
            "Previous Station": "Block 5",
            "Engine Failure": False,
            "Signal Pickup Failure": True,
            "Brake Failure": False,
            "Power": "80 kW",
            "Passenger Emergency Brake": "Off",
        }

        for i, (word_placeholder, value) in enumerate(
            zip(self.word_list_2, default_values_wordlist_2.values())
        ):
            label_text = f"{word_placeholder} {value}" if word_placeholder else value
            self.word_labels[i].setText(label_text)

    def update_wordlist2_values(self):
        values_wordlist_1 = self.apply_values()

        for i, word_placeholder in enumerate(self.word_list_2):
            if word_placeholder in self.values_2:
                label = self.values_2[word_placeholder]

                # Check if there is a corresponding label in word list 1
                corresponding_label = self.get_corresponding_label(word_placeholder)

                if corresponding_label:
                    # Get the value from word list 1 and format the label
                    value = values_wordlist_1.get(corresponding_label, "")
                    label = f"{word_placeholder} {value}"

                self.word_labels[i].setText(label)

    def get_corresponding_label(self, label_wordlist2):
        # Define a mapping between word list 2 labels and their corresponding word list 1 labels
        label_mapping = {
            "Speed Limit:": "Speed Limit:",
            "Authority:": "Authority:",
        }

        # Get the corresponding label from the mapping
        return label_mapping.get(label_wordlist2, "")

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)


class TrainControllerTestWindow(QMainWindow):
    def __init__(self, clock):
        super().__init__()
        self.setWindowTitle("Train Controller Test")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.clock = clock

        # Create a label for the clock in the main window
        self.font = QFont()
        self.font.setPointSize(20)
        self.clock_label = QLabel(self.central_widget)
        self.clock_label.setObjectName("clock_label")
        self.clock_label.setFont(self.font)
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Connect the clock's timeUpdated signal to the update_clock_label method
        self.clock.timeUpdated.connect(self.update_clock_label)

        # Start a timer to update the clock label periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock_label)
        self.timer.start(100)

        # Add the clock label to the central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.clock_label)
        self.layout.addStretch()

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName("TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName("TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Train Controller Test", self.central_widget)
        self.Title.setObjectName("Title")
        font = QFont()
        font.setFamilies(["Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(
            QCoreApplication.translate("TrainTest", "Train Controller Test", None)
        )
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName("mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap("src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Create a QLabel for the first rectangle
        self.rectangle_label = QLabel(self.central_widget)
        self.rectangle_label.setGeometry(QRect(50, 170, 590, 500))
        self.rectangle_label.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the blue and white backgrounds
        self.background_widget = QWidget(self.rectangle_label)
        self.background_widget.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget
        self.background_layout = QVBoxLayout(self.background_widget)
        self.background_layout.setContentsMargins(0, 0, 0, 0)
        self.background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.white_background_label = QLabel(self.central_widget)
        self.white_background_label.setGeometry(QRect(50, 210, 590, 430))
        self.white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header
        self.white_background_layout = QVBoxLayout(self.white_background_label)
        self.white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        word_list_1 = [
            "Passenger Emergency Brake:",
            "Temperature:",
            "Power:",
            "Commanded Speed:",
            "Setpoint Command:",
            "Announcements:",
            "Internal Lights:",
            "Headlights:",
            "Left Door:",
            "Right Door:",
            "Advertisements:",
        ]

        # Create and add QLineEdit widgets for the first word list
        self.value_inputs = {}
        for word_placeholder in word_list_1:
            word_label = QLabel(word_placeholder, self.white_background_label)
            word_label.setStyleSheet(
                "color: #000000; background-color: transparent; border: none;"
            )
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))

            value_input = QLineEdit(self.white_background_label)
            value_input.setStyleSheet(
                "background-color: #FFFFFF; border: 0.5px solid #000000;"
            )
            value_input.setContentsMargins(15, 15, 15, 15)

            word_layout = QHBoxLayout()
            word_layout.addWidget(word_label, alignment=Qt.AlignLeft)
            word_layout.addWidget(value_input, alignment=Qt.AlignLeft)

            self.white_background_layout.addLayout(word_layout)

            self.value_inputs[word_placeholder] = value_input

        self.white_background_layout.addStretch(1)

        # Create Apply and Reset buttons
        self.apply_button = QPushButton("Apply", self.central_widget)
        self.apply_button.setGeometry(1100, 640, 80, 30)
        self.apply_button.clicked.connect(self.apply_values)
        self.apply_button.setEnabled(True)

        self.reset_button = QPushButton("Reset", self.central_widget)
        self.reset_button.setGeometry(1190, 640, 80, 30)
        self.reset_button.clicked.connect(self.reset_values)
        self.reset_button.setEnabled(True)

        # Create the title label
        self.title_label = QLabel("Inputs:", self.rectangle_label)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator = QFrame(self.rectangle_label)
        self.line_separator.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator.setFrameShape(QFrame.HLine)
        self.line_separator.setFrameShadow(QFrame.Sunken)
        self.line_separator.setStyleSheet("background-color: #000000")

        # Create a QLabel for the second rectangle
        self.rectangle_label_2 = QLabel(self.central_widget)
        self.rectangle_label_2.setGeometry(QRect(640, 170, 590, 500))
        self.rectangle_label_2.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the red and white backgrounds
        self.background_widget_2 = QWidget(self.rectangle_label_2)
        self.background_widget_2.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget_2.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget
        self.white_background_layout_2 = QVBoxLayout(self.background_widget_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(0)

        # Create a QLabel for the white background below the red
        self.white_background_label_2 = QLabel(self.central_widget)
        self.white_background_label_2.setGeometry(QRect(640, 210, 590, 430))
        self.white_background_label_2.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header
        self.white_background_layout_2 = QVBoxLayout(self.white_background_label_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(5)

        # Create QLabel widgets for the list of words
        self.word_list_2 = [
            "Speed Limit:",
            "Authority:",
            "Commanded Speed:",
            "Current Speed:",
            "Temperature:",
            "Passengers Currently:",
            "Max Passengers:",
            "Next Station:",
            "Previous Station:",
            "Engine Failure:",
            "Signal Pickup Failure:",
            "Brake Failure:",
            "Power:",
            "Passenger Emergency Brake:",
        ]

        # Defines a dictionary with actual values for second set of words
        self.values_2 = {
            "Speed Limit:": "40 mph",
            "Authority:": "6 Blocks",
            "Commanded Speed:": "37 mph",
            "Current Speed:": "35 mph",
            "Temperature:": "78 ℉",
            "Passengers Currently:": "58",
            "Max Passengers:": "72",
            "Next Station:": "Block 7",
            "Previous Station:": "Block 3",
            "Engine Failure:": True,
            "Signal Pickup Failure:": False,
            "Brake Failure:": True,
            "Power:": "83 kW",
            "Passenger Emergency Brake:": "On",
        }

        # Initialize the list at the beginning of my method
        self.word_labels = []

        for word_placeholder in self.word_list_2:
            value = self.values_2.get(word_placeholder, "")
            label_text = f"{word_placeholder} {value}"
            word_label = QLabel(label_text, self.white_background_label_2)
            word_label.setStyleSheet(
                "color: #000000; background-color: transparent; border: none;"
            )
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))
            self.white_background_layout_2.addWidget(word_label, alignment=Qt.AlignTop)
            self.word_labels.append(word_label)

        # Create the title label
        self.title_label_2 = QLabel("Outputs:", self.rectangle_label_2)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label_2.setFont(self.font)
        self.title_label_2.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.title_label_2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label_2.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)
        self.line_separator_2.setStyleSheet("background-color: #000000")

    def apply_values(self):
        values_wordlist_1 = {}

        # Iterate through the input text boxes and update values_wordlist_1
        for word_placeholder, value_input in self.value_inputs.items():
            input_value = value_input.text()
            if input_value:
                try:
                    # Try to convert the input to an integer
                    input_value = int(input_value)
                except ValueError:
                    pass  # If it's not a valid integer, keep it as a string
                values_wordlist_1[word_placeholder] = input_value

        # Update the corresponding output values based on the mappings
        for word_placeholder, output_key in self.mapping.items():
            if word_placeholder in values_wordlist_1:
                self.values_2[output_key] = values_wordlist_1[word_placeholder]
                # Update the corresponding text box in the second set
                self.update_wordlist2_textbox(
                    output_key, values_wordlist_1[word_placeholder]
                )

        return values_wordlist_1

    def reset_values(self):
        default_values_wordlist_2 = {
            "Speed Limit": "45 mph",
            "Authority": "5 Blocks",
            "Commanded Speed": "35 mph",
            "Current Speed": "32 mph",
            "Temperature": "75 ℉",
            "Passengers Currently": "60",
            "Max Passengers": "74",
            "Next Station": "Block 9",
            "Previous Station": "Block 5",
            "Engine Failure": False,
            "Signal Pickup Failure": True,
            "Brake Failure": False,
            "Power": "80 kW",
            "Passenger Emergency Brake": "Off",
        }

        for i, (word_placeholder, value) in enumerate(
            zip(self.word_list_2, default_values_wordlist_2.values())
        ):
            label_text = f"{word_placeholder} {value}" if word_placeholder else value
            self.word_labels[i].setText(label_text)

    def update_wordlist2_values(self):
        values_wordlist_1 = self.apply_values()

        for i, word_placeholder in enumerate(self.word_list_2):
            if word_placeholder in self.values_2:
                label = self.values_2[word_placeholder]

                # Check if there is a corresponding label in word list 1
                corresponding_label = self.get_corresponding_label(word_placeholder)

                if corresponding_label:
                    # Get the value from word list 1 and format the label
                    value = values_wordlist_1.get(corresponding_label, "")
                    label = f"{word_placeholder} {value}"

                self.word_labels[i].setText(label)

    def get_corresponding_label(self, label_wordlist2):
        # Define a mapping between word list 2 labels and their corresponding word list 1 labels
        label_mapping = {"Passenger Emergency Brake:": "Passenger Emergency Brake"}

        # Get the corresponding label from the mapping
        return label_mapping.get(label_wordlist2, "")

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)

    def update_current_speed(self):
        if "Commanded Speed:" in self.values_2:
            commanded_speed = self.values_2["Commanded Speed:", 0]
            if self.current_speed < commanded_speed:
                acceleration = 0.5
                change = acceleration / 10
                self.current_speed = min(commanded_speed, self.current_speed + change)
            elif self.current_speed > commanded_speed:
                change = 0.1
                self.current_speed = max(commanded_speed, self.current_speed - change)

            # Update the current speed label
            self.current_speed_label.setText(f"Current Speed: {self.current_speed}")


class MurphyTestWindow(QMainWindow):
    def __init__(self, clock):
        super().__init__()
        self.setWindowTitle("Murphy Test")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.clock = clock

        # Create a label for the clock in the main window
        self.font = QFont()
        self.font.setPointSize(20)
        self.clock_label = QLabel(self.central_widget)
        self.clock_label.setObjectName("clock_label")
        self.clock_label.setFont(self.font)
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Connect the clock's timeUpdated signal to the update_clock_label method
        self.clock.timeUpdated.connect(self.update_clock_label)

        # Start a timer to update the clock label periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock_label)
        self.timer.start(100)

        # Add the clock label to the central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.clock_label)
        self.layout.addStretch()

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName("TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName("TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Murphy Test", self.central_widget)
        self.Title.setObjectName("Title")
        font = QFont()
        font.setFamilies(["Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(QCoreApplication.translate("TrainTest", "Murphy Test", None))
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName("mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap("src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Create a QLabel for the first rectangle
        self.rectangle_label = QLabel(self.central_widget)
        self.rectangle_label.setGeometry(QRect(50, 170, 590, 500))
        self.rectangle_label.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the blue and white backgrounds
        self.background_widget = QWidget(self.rectangle_label)
        self.background_widget.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget
        self.background_layout = QVBoxLayout(self.background_widget)
        self.background_layout.setContentsMargins(0, 0, 0, 0)
        self.background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.white_background_label = QLabel(self.central_widget)
        self.white_background_label.setGeometry(QRect(50, 210, 590, 430))
        self.white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header
        self.white_background_layout = QVBoxLayout(self.white_background_label)
        self.white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        word_list_1 = ["Engine Failure:", "Signal Pickup Failure:", "Brake Failure:"]

        values_1 = {
            "engine_failure": True,
            "signal_pickup_failure": False,
            "brake_failure": True,
        }

        # Create a vertical layout to place each pair of label and toggle switch
        vertical_layout = QVBoxLayout()

        for word_placeholder in word_list_1:
            # Create a widget that will hold the label and toggle switch vertically
            widget = QWidget()
            widget.setStyleSheet("background-color: transparent; border: none;")
            status_label = QLabel(word_placeholder, widget)
            status_label.setStyleSheet(
                "background: transparent; border: none;"
            )  # Remove background and border
            status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            status_label.setFont(QFont("Arial", 10))

            # Check if the word_placeholder is in the values_2 dictionary and is a boolean value
            if word_placeholder.lower().replace(":", "").replace(
                " ", "_"
            ) in values_1 and isinstance(
                values_1[word_placeholder.lower().replace(":", "").replace(" ", "_")],
                bool,
            ):
                # Create a custom toggle switch for the value
                toggle_switch = AnimatedToggle(
                    checked_color="red"
                )  # You can also use 'Toggle' for a non-animated version
                toggle_switch.setChecked(
                    values_1[
                        word_placeholder.lower().replace(":", "").replace(" ", "_")
                    ]
                )
                toggle_switch.setStyleSheet(
                    "background: transparent; border: none;"
                )  # Remove background and border
                toggle_switch.setFixedSize(60, 30)  # Adjust the size as needed
                toggle_switch.setContentsMargins(
                    5, 0, 5, 0
                )  # Adjust margins to remove spacing

                # Set the layout for the widget
                layout = QHBoxLayout()
                layout.addWidget(status_label)
                layout.addWidget(toggle_switch)
                layout.setAlignment(Qt.AlignLeft)

                widget.setLayout(layout)
            else:
                # For other options, use a QLabel to display the value
                value = (
                    "On"
                    if values_1.get(
                        word_placeholder.lower().replace(":", "").replace(" ", "_"),
                        False,
                    )
                    else "Off"
                )
                value_label = QLabel(value, widget)
                value_label.setStyleSheet("background: transparent; border: none;")
                value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                value_label.setFont(QFont("Arial", 10))

                # Set the layout for the widget
                layout = QHBoxLayout()
                layout.addWidget(status_label)
                layout.addWidget(value_label)

                widget.setLayout(layout)

            # Add the widget to the vertical layout
            vertical_layout.addWidget(widget)

        # Add the vertical layout to your main layout
        self.white_background_layout.addLayout(vertical_layout)

        # Create Apply and Reset buttons
        self.apply_button = QPushButton("Apply", self.central_widget)
        self.apply_button.setGeometry(1100, 640, 80, 30)
        self.apply_button.clicked.connect(self.apply_values)
        self.apply_button.setEnabled(True)

        self.reset_button = QPushButton("Reset", self.central_widget)
        self.reset_button.setGeometry(1190, 640, 80, 30)
        self.reset_button.clicked.connect(self.reset_values)
        self.reset_button.setEnabled(True)

        # Create the title label
        self.title_label = QLabel("Inputs:", self.rectangle_label)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator = QFrame(self.rectangle_label)
        self.line_separator.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator.setFrameShape(QFrame.HLine)
        self.line_separator.setFrameShadow(QFrame.Sunken)
        self.line_separator.setStyleSheet("background-color: #000000")

        # Create a QLabel for the second rectangle
        self.rectangle_label_2 = QLabel(self.central_widget)
        self.rectangle_label_2.setGeometry(QRect(640, 170, 590, 500))
        self.rectangle_label_2.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the red and white backgrounds
        self.background_widget_2 = QWidget(self.rectangle_label_2)
        self.background_widget_2.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget_2.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget
        self.white_background_layout_2 = QVBoxLayout(self.background_widget_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(0)

        # Create a QLabel for the white background below the red
        self.white_background_label_2 = QLabel(self.central_widget)
        self.white_background_label_2.setGeometry(QRect(640, 210, 590, 430))
        self.white_background_label_2.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header
        self.white_background_layout_2 = QVBoxLayout(self.white_background_label_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(5)

        # Create QLabel widgets for the list of words
        self.word_list_2 = [
            "Speed Limit:",
            "Authority:",
            "Commanded Speed:",
            "Current Speed:",
            "Temperature:",
            "Passengers Currently:",
            "Max Passengers:",
            "Next Station:",
            "Previous Station:",
            "Engine Failure:",
            "Signal Pickup Failure:",
            "Brake Failure:",
            "Power:",
            "Passenger Emergency Brake:",
        ]

        # Defines a dictionary with actual values for second set of words
        self.values_2 = {
            "Speed Limit:": "40 mph",
            "Authority:": "6 Blocks",
            "Commanded Speed:": "37 mph",
            "Current Speed:": "35 mph",
            "Temperature:": "78 ℉",
            "Passengers Currently:": "58",
            "Max Passengers:": "72",
            "Next Station:": "Block 7",
            "Previous Station:": "Block 3",
            "Engine Failure:": True,
            "Signal Pickup Failure:": False,
            "Brake Failure:": True,
            "Power:": "83 kW",
            "Passenger Emergency Brake:": "On",
        }

        # Initialize the list at the beginning of my method
        self.word_labels = []

        for word_placeholder in self.word_list_2:
            value = self.values_2.get(word_placeholder, "")
            label_text = f"{word_placeholder} {value}"
            word_label = QLabel(label_text, self.white_background_label_2)
            word_label.setStyleSheet(
                "color: #000000; background-color: transparent; border: none;"
            )
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))
            self.white_background_layout_2.addWidget(word_label, alignment=Qt.AlignTop)
            self.word_labels.append(word_label)

        # Create the title label
        self.title_label_2 = QLabel("Outputs:", self.rectangle_label_2)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label_2.setFont(self.font)
        self.title_label_2.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.title_label_2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label_2.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)
        self.line_separator_2.setStyleSheet("background-color: #000000")

    def apply_values(self):
        values_wordlist_1 = {}

        # Iterate through the input text boxes and update values_wordlist_1
        for word_placeholder, value_input in self.value_inputs.items():
            input_value = value_input.text()
            if input_value:
                try:
                    # Try to convert the input to an integer
                    input_value = int(input_value)
                except ValueError:
                    pass  # If it's not a valid integer, keep it as a string
                values_wordlist_1[word_placeholder] = input_value

        # Update the corresponding output values based on the mappings
        for word_placeholder, output_key in self.mapping.items():
            if word_placeholder in values_wordlist_1:
                self.values_2[output_key] = values_wordlist_1[word_placeholder]
                # Update the corresponding text box in the second set
                self.update_wordlist2_textbox(
                    output_key, values_wordlist_1[word_placeholder]
                )

        return values_wordlist_1

    def reset_values(self):
        default_values_wordlist_2 = {
            "Speed Limit": "45 mph",
            "Authority": "5 Blocks",
            "Commanded Speed": "35 mph",
            "Current Speed": "32 mph",
            "Temperature": "75 ℉",
            "Passengers Currently": "60",
            "Max Passengers": "74",
            "Next Station": "Block 9",
            "Previous Station": "Block 5",
            "Engine Failure": False,
            "Signal Pickup Failure": True,
            "Brake Failure": False,
            "Power": "80 kW",
            "Passenger Emergency Brake": "Off",
        }

        for i, (word_placeholder, value) in enumerate(
            zip(self.word_list_2, default_values_wordlist_2.values())
        ):
            label_text = f"{word_placeholder} {value}" if word_placeholder else value
            self.word_labels[i].setText(label_text)

    def update_wordlist2_values(self, reset=False):
        values_wordlist_1 = self.apply_values()

        for i, word_placeholder in enumerate(self.word_list_2):
            if word_placeholder in self.values_2:
                label = self.values_2[word_placeholder]

                # Check if there is a corresponding label in word list 1
                corresponding_label = self.get_corresponding_label(word_placeholder)

                if corresponding_label:
                    # Get the value from word list 1 and format the label
                    value = values_wordlist_1.get(corresponding_label, "")
                    label = f"{word_placeholder} {value}"

                self.word_labels[i].setText(label)

    def get_corresponding_label(self, label_wordlist2):
        # Define a mapping between word list 2 labels and their corresponding word list 1 labels
        label_mapping = {
            "Engine Failure:": "Engine Failure:",
            "Signal Pickup Failure:": "Signal Pickup Failure",
            "Brake Failure:": "Brake Failure",
        }

        # Get the corresponding label from the mapping
        return label_mapping.get(label_wordlist2, "")

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)


# class Calculations:
#     def __init__(self, time_interval, sys_time, trains):
#         self.time_interval = time_interval
#         self.sys_time = sys_time
#         self.trains = trains

#     # Sets the power of the train through the train controller
#     def power(self, trainObject, power):
#         # Ensure that power does not exceed 120
#         power /= 1000
#         currPower = min(power, 120)

#         # Update the "vehicle_status" of "Train 1" in self.trains
#         trainObject.vehicle_status["power"] = currPower

#         # Calculate current_speed using the updated power
#         self.current_speed(trainObject, currPower)

#     def current_speed(self, trainObject, currPower):
#         # Retrieve necessary values from self.trains
#         lastVelocity = trainObject.calculations["lastVelocity"]
#         mass = trainObject.calculations["mass"]

#         if lastVelocity == 0:
#             lastVelocity = 0.001

#         currForce = currPower / lastVelocity

#         # Set calculated force and apply force limit
#         trainObject.calculations["currForce"] = currForce

#         self.limit_force(trainObject)

#         # Calculate acceleration from force and set it, applying acceleration limit
#         trainObject.calculations["currAcceleration"] = trainObject.calculations["currForce"] / mass
#         currAcceleration = self.limit_acceleration(trainObject)

#         # Calculate velocity using the velocity function and set it
#         currVelocity = self.velocity()
#         self.trains.set_value("Train 1", "calculations", "currVelocity", currVelocity)

#         # Calculate the distance traveled and set it
#         new_position = self.total_distance()

#         # Return the current velocity
#         return currVelocity

#     def limit_force(self, trainObject):
#         # Retrieve necessary values from self.trains
#         emergency_brake = trainObject.failure_status["emergency_brake"]
#         mass = trainObject.calculations["mass"]
#         force = trainObject.calculations["currForce"]
#         power = trainObject.vehicle_status["power"]
#         lastVelocity = trainObject.calculations["lastVelocity"]

#         # Limit the force of the train
#         if force > (mass * 0.5):
#             force = mass * 0.5
#         elif (power == 0 and lastVelocity == 0) or emergency_brake:
#             force = 0
#         elif lastVelocity == 0:
#             force = mass * 0.5

#         # Set the limited force value
#         trainObject.calculations["currForce"] = force

#     def limit_acceleration(self, trainObject):
#         # Retrieve necessary values from self.trains
#         failure_1 = trainObject.failure_status["engine_failure"]
#         failure_2 = trainObject.failure_status["signal_pickup_failure"]
#         failure_3 = trainObject.failure_status["brake_failure"]
#         brakes = trainObject.vehicle_status["brakes"]
#         emergency_brake = self.trains.get_value("Train 1", "failure_status", "emergency_brake")
#         force = self.trains.get_value("Train 1", "calculations", "currForce")
#         mass = self.trains.get_value("Train 1", "calculations", "mass")
#         power = self.trains.get_value("Train 1", "vehicle_status", "power")
#         currVelocity = self.trains.get_value("Train 1", "calculations", "currVelocity")

#         # Limit the acceleration of the train based on various conditions
#         if (failure_1 or failure_2 or failure_3) and (brakes or emergency_brake):
#             acceleration = (force - (0.01 * mass * 9.8)) / mass
#         elif power == 0 and currVelocity > 0:
#             if emergency_brake:
#                 acceleration = -2.73
#             else:
#                 acceleration = -1.2
#         elif power != 0:
#             if force > 0.5:
#                 acceleration = 0.5
#             else:
#                 acceleration = force / mass
#         else:
#             acceleration = 0

#         # Set the limited acceleration value
#         self.trains.set_value("Train 1", "calculations", "currAcceleration", acceleration)

#         return acceleration

#     def velocity(self):
#         # Retrieve necessary values from self.trains
#         brake = self.trains.get_value("Train 1", "vehicle_status", "brakes")
#         emergency_brake = self.trains.get_value("Train 1", "failure_status", "emergency_brake")
#         last_acceleration = self.trains.get_value("Train 1", "calculations", "lastAcceleration")
#         curr_acceleration = self.trains.get_value("Train 1", "calculations", "currAcceleration")
#         last_velocity = self.trains.get_value("Train 1", "calculations", "lastVelocity")

#         # Calculate the total acceleration and update velocity
#         total_acceleration = last_acceleration + curr_acceleration
#         velocity = last_velocity + (self.time_interval / 2) * total_acceleration

#         # Limit velocity so that it doesn't go below 0
#         if velocity < 0:
#             velocity = 0

#         # If the train is stopped and brakes or emergency brake are applied, set velocity to 0
#         if last_velocity <= 0 and (brake or emergency_brake):
#             velocity = 0

#         # Set the calculated velocity value
#         velocity = self.trains.set_value("Train 1", "calculations", "currVelocity", velocity)

#         return velocity

#     def total_distance(self):
#         # Retrieve necessary values from self.trains
#         curr_velocity = self.trains.get_value("Train 1", "calculations", "currVelocity")
#         last_position = self.trains.get_value("Train 1", "calculations", "lastPosition")

#         # Update total_velocity using the current velocity (consider whether this is necessary)
#         total_velocity = curr_velocity

#         # Correct the distance calculation (multiply, not divide)
#         distance = last_position + (self.time_interval * 2) * total_velocity

#         return distance

#     def blockID(
#             self, next_block, length, grade, speed_limit, suggested_speed, authority
#     ):
#         self.trains.set_value("Train 1", "calculations", "nextBlock", next_block)
#         self.trains.set_value("Train 1", "navigation_status", "length", length)
#         self.trains.set_value("Train 1", "navigation_status", "grade", grade)
#         self.trains.set_value("Train 1", "vehicle_status", "speed_limit", speed_limit)
#         self.trains.set_value("Train 1", "vehicle_status", "suggested_speed", suggested_speed)
#         self.trains.set_value("Train 1", "navigation_status", "authority", authority)

#         train = self.trains.get_value("Train 1", "calculations", "trainID")

#         self.occupancy(next_block)

#         # Send train controller information
#         trainModelToTrainController.sendBlockLength.emit(length)
#         trainModelToTrainController.sendSpeedLimit.emit(train, speed_limit)
#         trainModelToTrainController.sendCommandedSpeed.emit(train, suggested_speed)
#         trainModelToTrainController.sendAuthority.emit(train, authority)

#         return next_block, length, grade, speed_limit, suggested_speed, authority

#     def failures(self):
#         engine_failure = self.trains.get_value("Train 1", "failure_status", "engine_failure")
#         signal_pickup_failure = self.trains.get_value("Train 1", "failure_status", "signal_pickup_failure")
#         brake_failure = self.trains.get_value("Train 1", "failure_status", "brake_failure")
#         pass_emergency_brake = self.trains.get_value("Train 1", "failure_status", "passenger_emergency_brake")
#         train = self.trains.get_value("Train 1", "calculations", "trainID")

#         if (
#                 engine_failure == True
#                 or signal_pickup_failure == True
#                 or brake_failure == True
#         ):
#             trainModelToTrainController.sendEngineFailure.emit(train, engine_failure)
#             trainModelToTrainController.sendSignalPickupFailure.emit(
#                 train, signal_pickup_failure
#             )
#             trainModelToTrainController.sendBrakeFailure.emit(train, brake_failure)

#         if pass_emergency_brake == True:
#             trainModelToTrainController.sendPassengerEmergencyBrake.emit(
#                 train, pass_emergency_brake
#             )

#         return (
#             engine_failure,
#             signal_pickup_failure,
#             brake_failure,
#             pass_emergency_brake,
#         )

#     def temperature(self, temp):
#         set_temp = temp
#         curr_temp = self.trains.get_value("Train 1", "vehicle_status", "temperature")
#         train = self.trains.get_value("Train 1", "calculations", "trainID")

#         if curr_temp < set_temp:
#             while curr_temp < set_temp:
#                 curr_temp += 1
#                 self.trains.set_value("Train 1", "vehicle_status", "temperature", curr_temp)
#                 trainModelToTrainController.sendTemperature.emit(train, curr_temp)

#         elif set_temp > curr_temp:
#             while curr_temp > set_temp:
#                 curr_temp -= 1
#                 self.trains.set_value("Train 1", "vehicle_status", "temperature", curr_temp)
#                 trainModelToTrainController.sendTemperature.emit(train, curr_temp)

#         elif set_temp == curr_temp:
#             self.trains.set_value("Train 1", "vehicle_status", "temperature", curr_temp)
#             trainModelToTrainController.sendTemperature.emit(train, curr_temp)

#         return curr_temp

#     # Calculate the current number of passengers from the track model
#     def passengers(self, passengers):
#         curr_passengers = self.trains.get_values("Train 1", "passenger_status", "passengers")
#         trainModelToTrackModel.sendCurrentPassengers.emit(curr_passengers, "Train 1")

#         self.trains.set_values("Train 1", "passenger_status", "passengers", passengers)

#         return passengers

#     def occupancy(self, next_block):
#         distance = 0
#         polarity = 0
#         initialized = 0
#         # distance = self.total_distance()
#         block_length = self.trains.get_value("Train 1", "navigation_status", "block_length")
#         next_block = self.trains.set_value("Train 1", "calculations", "nextBlock", next_block)
#         curr_block = self.trains.get_value("Train 1", "calculations", "currBlock")
#         prev_block = self.trains.get_value("Train 1", "calculations", "prevBlock")
#         trainID = self.trains.get_value("Train 1", "calculations", "trainID")
#         line = self.trains.get_value("Train 1", "calculations", "line")

#         if initialized == 0:
#             trainModelToTrackModel.sendPolarity.emit(line, curr_block, prev_block)

#         if distance == block_length:
#             distance = 0
#             polarity = 1
#             trainModelToTrackModel.sendPolarity.emit(line, curr_block, prev_block)
#             trainModelToTrainController.sendPolarity.emit(trainID, polarity)

#             curr_block = next_block
#             prev_block = curr_block

#         initialized += 1
#         if initialized >= 999:
#             initialized = 1

#     def beacon(self, beacon):
#         next_station1 = beacon["Next Station1"]
#         next_station2 = beacon["Next Station2"]
#         current_station = beacon["Current Station"]
#         door_side = beacon["Door Side"]
#         train = self.trains.get_value("Train 1", "calculations", "trainID")

#         trainModelToTrainController.sendNextStation1.emit(train, next_station1)
#         trainModelToTrainController.sendNextStation2.emit(train, next_station2)
#         trainModelToTrainController.sendCurrStation.emit(train, current_station)

#         if door_side == "Left":
#             trainModelToTrainController.sendLeftDoor.emit(train, door_side)
#         elif door_side == "Right":
#             trainModelToTrainController.sendRightDoor.emit(train, door_side)
#         else:
#             trainModelToTrainController.sendLeftDoor.emit(train, door_side)
#             trainModelToTrainController.sendRightDoor.emit(train, door_side)

#         return next_station1, next_station2, current_station, door_side

# def main():
#     app = QApplication(sys.argv)
#     ui = TrainModel()
#     ui.show_gui()
#     sys.exit(app.exec_())


# if __name__ == "__main__":
#     main()
