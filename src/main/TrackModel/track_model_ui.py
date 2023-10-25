import sys
import re
import load_track
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#DONE :)
class FailureWindow():
    selected_block = None
    selected_failures = []
    
    def __init__(self):
        self.failure_window = QDialog()
        self.setup_failure_popup()
        
    def setup_failure_popup(self):
        self.failure_window.setWindowTitle("Change Failures")
        self.failure_window.setGeometry(1550, 500, 250, 300)
        self.failure_window.setStyleSheet("background-color: #ff4747;")
        
        self.failure_title()
        self.change_background()
        self.add_block_selection()
        self.add_failure_selection()
        self.add_set_button()
    
    def failure_title(self):
        title = QLabel("Failure Configuration:", self.failure_window)
        title.setGeometry(10, 10, 230, 30)
        title.setStyleSheet("font-weight: bold; font-size: 18px")
        
        #Horizontal divider line
        thickness = 5
        hline = QFrame(self.failure_window)
        hline.setFrameShape(QFrame.HLine)
        hline.setGeometry(0, 40, 250, thickness)
        hline.setLineWidth(thickness)
    
    def change_background(self):
        background = QWidget(self.failure_window)
        background.setGeometry(0, 45, 250, 300)
        background.setStyleSheet("background-color: #ffd6d6;")
        
    def add_block_selection(self):
        select_block = QLabel("Select Block #:", self.failure_window)
        select_block.setGeometry(10, 50, 230, 30)
        select_block.setStyleSheet("font-weight: bold; font-size: 18px; background-color: #ffd6d6;")
        
        # Add a dropdown selection
        self.block_dropdown = QComboBox(self.failure_window)
        self.block_dropdown.setGeometry(10, 80, 115, 30)
        self.block_dropdown.setStyleSheet("background-color: white;")
        for i in range(1, 16):
            self.block_dropdown.addItem("Block " + str(i))
        
        self.block_dropdown.currentIndexChanged.connect(self.update_exit_button_state)
    
    def add_failure_selection(self):
        set_failure = QLabel("Set Failure Type:", self.failure_window)
        set_failure.setGeometry(10, 120, 230, 30)
        set_failure.setStyleSheet("font-weight: bold; font-size: 18px; background-color: #ffd6d6")

        self.failure_checkboxes = []
        failures = [
            "Track Circuit Failure",
            "Power Failure",
            "Broken Rail"
        ]
        y_offset = 150
        for failure in failures:
            option = QCheckBox(failure, self.failure_window)
            option.setGeometry(10, y_offset, 230, 30)
            option.setStyleSheet("background-color: #ffd6d6")
            self.failure_checkboxes.append(option)
            y_offset += 30

    def update_exit_button_state(self):
        #Enable the button to "Set Failure Configuration" if a drop down item from the menu is selected
        is_block_selected = self.block_dropdown.currentIndex() != -1
        self.button.setEnabled(is_block_selected)

    def add_set_button(self):
        self.button = QPushButton("Set Failure Configuration", self.failure_window)
        self.button.setGeometry(50, 250, 150, 30)
        self.button.setStyleSheet("background-color: #39E75F;")
        self.button.clicked.connect(self.update_failure)
        self.button.setEnabled(False) #Button is set as disabled to begin with
    
    def update_failure(self):
        selected_block_index = self.block_dropdown.currentIndex()
        selected_block = self.block_dropdown.itemText(selected_block_index)

        self.selected_failures.clear()
        for checkbox in self.failure_checkboxes:
            if checkbox.isChecked():
                self.selected_failures.append(checkbox.text())
        self.selected_block = selected_block

        self.failure_window.close()
    
    def get_selected_block(self):
        if self.selected_block != None:
            #Pull block int from string
            pattern = r'\d+'
            search_int = re.search(pattern, self.selected_block)
            if search_int:
                block_num = int(search_int.group())
                return block_num
        
    def get_selected_failures(self):
        if self.selected_failures == []:
            return "None"
        return self.selected_failures
                
class SelectionWindow():
    simulation_speed = 1.0
    selected_line = None
    temperature = 65
    allowable_directions = "EAST/WEST"
    track_heater = "OFF"
    failures = "None"
    beacon = "---"
    ticket_sales = 0
    waiting = 0

    def __init__(self):
        self.setup_selection_window()
      
    def setup_selection_window(self):
        app = QApplication(sys.argv)
        mainWindow = QWidget()
        mainWindow.setGeometry(350,200,1200,750)
        mainWindow.setWindowTitle("Track Model")
        app.setWindowIcon(QIcon("src/main/TrackModel/pngs/MTA_logo.png"))
        
        #General layout
        self.add_mta_logo(mainWindow)
        self.set_clock(mainWindow)
        self.set_simulation_speed_controls(mainWindow)
        self.add_vline(mainWindow)
        self.add_hline(mainWindow)
        self.add_title(mainWindow)
        self.add_tabbar(mainWindow)
        
        #Map
        self.add_line_panel(mainWindow)
        self.control_temperature(mainWindow)
        self.add_import_button(mainWindow)
        #The following are hidden initially and are shown upon an excel file import
        self.display_file_path(mainWindow)
        self.add_track_map(mainWindow)
        self.add_map_zoom(mainWindow)
        self.add_map_pngs(mainWindow)
        
        self.add_block_info_display(mainWindow)
        self.add_station_info(mainWindow)
        
        #Block Info Selection
        self.add_input_section(mainWindow)
        self.add_selectable_block_info(mainWindow)
        self.add_change_failures_button(mainWindow)
        
        mainWindow.show()
        sys.exit(app.exec_())
        
    def add_mta_logo(self, parent_window):
        mta_png = QPixmap("src/main/TrackModel/pngs/mta_logo.png")
        mta_png = mta_png.scaledToWidth(90)
        mta_logo = QLabel(parent_window)
        mta_logo.setPixmap(mta_png)
        mta_logo.setGeometry(0, 0, mta_png.width(), mta_png.height())
              
    def set_clock(self, parent_window):
        self.clock = QLabel("System Clock: 00:00:00", parent_window)
        self.clock.setGeometry(980, 10, 220, 30)
        self.clock.setStyleSheet("font-weight: bold; font-size: 18px")
        self.update_clock()

        #Update clock in real time while window is open
        timer = QTimer(parent_window)
        timer.timeout.connect(self.update_clock)
        #Update every 1 second
        timer.start(1000)

    def update_clock(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_time = current_datetime.toString("HH:mm:ss")
        self.clock.setText("System Clock: " + formatted_time)
    
    def set_simulation_speed_controls(self, parent_window):
        simulation_speed_text = QLabel("Simulation Speed:", parent_window)
        simulation_speed_text.setGeometry(900, 50, 170, 30)
        simulation_speed_text.setStyleSheet("font-weight: bold; font-size: 18px")

        self.speed_text = QLabel("1.0x", parent_window)
        self.speed_text.setGeometry(1110, 50, 40, 30)
        self.speed_text.setAlignment(Qt.AlignCenter)
        self.speed_text.setStyleSheet("font-weight: bold; font-size: 18px")
        
        decrease_speed = QPushButton("<<", parent_window)
        decrease_speed.setGeometry(1070, 55, 30, 20)
        decrease_speed.clicked.connect(self.decrease_simulation_speed)

        increase_speed = QPushButton(">>", parent_window)
        increase_speed.setGeometry(1160, 55, 30, 20)
        increase_speed.clicked.connect(self.increase_simulation_speed)

    def decrease_simulation_speed(self):
        #Speed cannot go below 0.5
        if self.simulation_speed > 0.5:
            self.simulation_speed -= 0.5
            self.speed_text.setText(f"{self.simulation_speed}x")

    def increase_simulation_speed(self):
        if self.simulation_speed < 5.0:
            self.simulation_speed += 0.5
            self.speed_text.setText(f"{self.simulation_speed}x")
        
    def add_vline(self, parent_window):
        thickness = 5
        
        line = QFrame(parent_window)
        line.setFrameShape(QFrame.VLine)
        line.setGeometry(950, 100, thickness, 700)
        line.setLineWidth(thickness)
        
    def add_hline(self, parent_window):
        thickness = 5
        
        line = QFrame(parent_window)
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(0, 100, 1200, thickness)
        line.setLineWidth(thickness)
   
    def add_title(self, parent_window):        
        window_width = parent_window.width()
        label_width = 300
        title_position = int((window_width - label_width) / 2)
        
        title_label = QLabel("Track Model", parent_window)
        title_label.setGeometry(title_position, 35, label_width, 30)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)

    def add_line_panel(self, parent_window):
        select_line = QLabel("Select Line:", parent_window)
        select_line.setGeometry(90, 130, 110, 30)
        select_line.setStyleSheet("font-weight: bold; font-size: 18px")

        self.blue_panel = QLabel("Blue Line", parent_window)
        self.green_panel = QLabel("Green Line", parent_window)
        self.red_panel = QLabel("Red Line", parent_window)

        self.blue_panel.setGeometry(20, 160, 80, 30)
        self.green_panel.setGeometry(100, 160, 80, 30)
        self.red_panel.setGeometry(180, 160, 80, 30)
        
        #Initially greyed out as none are selected
        unselected = "background-color: grey; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
        self.blue_panel.setStyleSheet(unselected)
        self.green_panel.setStyleSheet(unselected)
        self.red_panel.setStyleSheet(unselected)

        #Handlers that call the select_line method
        self.blue_panel.mousePressEvent = lambda event, line="Blue Line": self.select_line(line)
        self.green_panel.mousePressEvent = lambda event, line="Green Line": self.select_line(line)
        self.red_panel.mousePressEvent = lambda event, line="Red Line": self.select_line(line)

    def select_line(self, selected_line):
        unselected = "background-color: grey; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
        if selected_line != self.selected_line:
            if selected_line == "Blue Line":
                self.blue_panel.setStyleSheet("background-color: blue; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;")
                self.green_panel.setStyleSheet(unselected)
                self.red_panel.setStyleSheet(unselected)
            elif selected_line == "Green Line":
                self.blue_panel.setStyleSheet(unselected)
                self.green_panel.setStyleSheet("background-color: green; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;")
                self.red_panel.setStyleSheet(unselected)
            elif selected_line == "Red Line":
                self.blue_panel.setStyleSheet(unselected)
                self.green_panel.setStyleSheet(unselected)
                self.red_panel.setStyleSheet("background-color: red; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;")
                
            self.selected_line = selected_line
            
    def control_temperature(self, parent_window):
        set_temperature = QLabel("Set Temperature:", parent_window)
        set_temperature.setGeometry(420, 130, 160, 30)
        set_temperature.setStyleSheet("font-weight: bold; font-size: 18px")

        self.temperature_input = QLineEdit(parent_window)
        self.temperature_input.setGeometry(440, 160, 40, 30)
        self.temperature_input.setAlignment(Qt.AlignCenter)
        self.temperature_input.setPlaceholderText("65")

        fahrenheit_unit = QLabel("°F", parent_window)
        fahrenheit_unit.setGeometry(480, 160, 30, 30)
        fahrenheit_unit.setStyleSheet("font-weight: bold; font-size: 14px")

        set_temperature_button = QPushButton("Set", parent_window)
        set_temperature_button.setGeometry(500, 160, 60, 30)
        set_temperature_button.setStyleSheet("background-color: blue; color: white")
        set_temperature_button.clicked.connect(self.set_temperature)

    def set_temperature(self):
        if self.temperature_input.text() != "":
            self.temperature = self.temperature_input.text()
        self.temperature_input.setPlaceholderText(str(self.temperature))
        print(self.temperature)

    def add_map_pngs(self, parent_window):
        self.switch_png = QLabel(parent_window)
        self.switch_png.setGeometry(450, 420, 30, 30)
        self.switch_png.setPixmap(QPixmap("src/main/TrackModel/pngs/train_track.png").scaled(25, 25))
        self.switch_png.hide()
        
        #Temp
        self.occ1_png = QLabel(parent_window)
        self.occ1_png.setGeometry(80, 422, 80, 60)
        self.occ1_png.setPixmap(QPixmap("src/main/TrackModel/pngs/occ1.png"))
        self.occ1_png.hide()
        
        self.occ10_png = QLabel(parent_window)
        self.occ10_png.setGeometry(707, 213, 80, 70)
        self.occ10_png.setPixmap(QPixmap("src/main/TrackModel/pngs/occ10.png"))
        self.occ10_png.mousePressEvent = self.update_station_display
        self.occ10_png.hide()
        #Add rest later
    
    def add_track_map(self, parent_window):
        self.map_png = QPixmap("src/main/TrackModel/pngs/blue_line.png")
        self.og_width, self.og_height = 950, 550
        self.map_width, self.map_height = self.og_width, self.og_height
        self.map_png = self.map_png.scaled(self.map_width, self.map_height)

        self.track_map = QLabel(parent_window)
        self.track_map.setPixmap(self.map_png)
        self.track_map.setGeometry(0, 200, self.map_width, self.map_height)
        self.track_map.hide()

    def add_map_zoom(self, parent_window):
        self.zoom_in_button = QPushButton("+", parent_window)
        self.zoom_in_button.setGeometry(910, 210, 30, 30)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_in_button.hide()

        self.zoom_out_button = QPushButton("-", parent_window)
        self.zoom_out_button.setGeometry(910, 240, 30, 30)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.hide()

    def zoom_in(self):
        self.map_width += 50
        self.map_height += 50
        self.map_png = self.map_png.scaled(self.map_width, self.map_height)
        self.track_map.setPixmap(self.map_png)

    def zoom_out(self):
        self.map_width -= 50
        self.map_height -= 50
        #Cannot zoom out past original size map
        self.map_width = max(self.map_width, self.og_width)
        self.map_height = max(self.map_height, self.og_height)
        self.map_png = self.map_png.scaled(self.map_width, self.map_height)
        self.track_map.setPixmap(self.map_png)    

    def display_file_path(self, parent_window):
        #Originally, nothing is shown
        self.file_path = QLabel("", parent_window)
        self.file_path.setGeometry(740, 130, 200, 30)
        self.file_path.setAlignment(Qt.AlignRight)
        self.file_path.setStyleSheet("color: #008000; font-size: 9px;")
        
    def update_file_path(self, file_path):
        #When file is selected, its path is shown
        self.file_path.setText("Selected File:\n" + file_path)
    
    def add_import_button(self, parent_window):
        import_png = QLabel(parent_window)
        import_png.setGeometry(790, 160, 30, 30)
        import_png.setPixmap(QPixmap("src/main/TrackModel/pngs/import_arrow.png").scaled(30, 30))
                
        import_button = QPushButton("Import Track Data", parent_window)
        import_button.setGeometry(820, 160, 120, 30)
        import_button.setStyleSheet("background-color: #39E75F;")
        #Need to call lambda as parent_window is not accessible otherwise
        import_button.clicked.connect(lambda: self.import_track_data(parent_window))

    def update_gui(self, file_path):
        self.update_file_path(file_path)
        self.select_line("Blue Line") #Sets label to blue as that is the only line
        self.track_map.show()
        self.zoom_in_button.show()
        self.zoom_out_button.show()
        self.zoom_in_button.setDisabled(True)
        self.zoom_out_button.setDisabled(True)
        self.change_failures_button.setEnabled(True)
        self.go_button.setEnabled(True)
        for checkbox in self.track_info_checkboxes.values():
            checkbox.setDisabled(False)
        
    def import_track_data(self, parent_window):
        options = QFileDialog.Options() | QFileDialog.ReadOnly
        #Opens file explorer in new customized window
        file_path, file_type = QFileDialog.getOpenFileName(parent_window, "Import Track Data", "", "Excel Files (*.xlsx *.xls)", options= options)
        
        if file_path:
            #Update Gui
            self.update_gui(file_path)
            
            self.track_data = load_track.read_track_data(file_path)
            #Add failures, set to default "None" to begin
            for block in self.track_data:
                block["Failures"] = self.failures
                
            print(self.track_data)
        
    def add_input_section(self, parent_window):
        label = QLabel("Enter Block #:", parent_window)
        label.setGeometry(970, 120, 150, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        
        self.entry_field = QLineEdit(parent_window)
        self.entry_field.setGeometry(970, 160, 100, 30)
        self.entry_field.setPlaceholderText("Enter block #")
        
        self.go_button = QPushButton("Go", parent_window)
        self.go_button.setGeometry(1080, 160, 60, 30)
        self.go_button.setStyleSheet("background-color: blue; color: white")
        # Connect the button to the update_block_info_display method
        self.go_button.clicked.connect(self.update_block_info_display)
        self.go_button.setEnabled(False)  # The button is disabled initially    
        
        self.error_label = QLabel("", parent_window)
        self.error_label.setGeometry(970, 185, 210, 30)
        self.error_label.setStyleSheet("color: red; font-size: 14px")   

    def add_block_info_display(self, parent_window):
        self.block_info_display = QTextEdit(parent_window)
        self.block_info_display.setGeometry(10, 550, 400, 160)
        self.block_info_display.setStyleSheet("background-color: white; font-size: 14px")
        self.block_info_display.setReadOnly(True)
        self.block_info_display.hide()
        
    def add_selectable_block_info(self, parent_window):
        label = QLabel("Block Information:", parent_window)
        label.setGeometry(970, 210, 200, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        
        self.block_info_checkboxes = {}
        block_info = [
            "Block Length", "Speed Limit", "Elevation", "Cumulative Elevation",
            "Block Grade", "Allowed Directions of Travel", "Track Heater",
            "Failures", "Beacon"
        ]
        y_offset = 240
        for info in block_info:
            checkbox = QCheckBox(info, parent_window)
            checkbox.setGeometry(980, y_offset, 200, 30)
            self.block_info_checkboxes[info] = checkbox
            y_offset += 30
            checkbox.setDisabled(True)
            checkbox.stateChanged.connect(self.update_block_info_display)
        
        self.track_info_checkboxes = {}
        track_info = [
            "Show Occupied Blocks", "Show Switches", 
            "Show Light Signals", "Show Railway Crossings"
        ]
        y_offset += 20
        for info in track_info:
            checkbox = QCheckBox(info, parent_window)
            checkbox.setGeometry(970, y_offset, 160, 30)
            self.track_info_checkboxes[info] = checkbox
            checkbox.setDisabled(True)
            if "Switch" in info:
                switch_png = QLabel(parent_window)
                switch_png.setGeometry(1080, y_offset, 30, 30)
                switch_png.setPixmap(QPixmap("src/main/TrackModel/pngs/train_track.png").scaled(25, 25))
            if "Light Signal" in info:
                light_signal_png = QLabel(parent_window)
                light_signal_png.setGeometry(1100, y_offset, 30, 30)
                light_signal_png.setPixmap(QPixmap("src/main/TrackModel/pngs/traffic_light.png").scaled(25, 25))
            if "Railway Crossing" in info:
                railway_crossing_png = QLabel(parent_window)
                railway_crossing_png.setGeometry(1130, y_offset, 30, 30)
                railway_crossing_png.setPixmap(QPixmap("src/main/TrackModel/pngs/railway_crossing.png").scaled(25, 25))
                
            y_offset += 30
        
        #Checkbox events
        show_switches_checkbox = self.track_info_checkboxes["Show Switches"]
        show_switches_checkbox.stateChanged.connect(self.change_switches_img)
        show_occupied_checkbox = self.track_info_checkboxes["Show Occupied Blocks"]
        show_occupied_checkbox.stateChanged.connect(self.change_occupied_img)
    
    def add_station_info(self, parent_window):
        self.station_info = QTextEdit("", parent_window)
        self.station_info.setGeometry(760, 300, 160, 70)
        self.station_info.setAlignment(Qt.AlignCenter)
        self.station_info.setStyleSheet("background-color: #d0efff; color: black; font-size: 14px")
        self.station_info.hide()
    
    def update_station_display(self, event):
        if self.station_info.isHidden():
            self.station_info.setText(
            f"<b>Blue Line</b>"
            f"<br>Ticket Sales/Hr: {self.ticket_sales}</br>"
            f"<br>Waiting @ Station B: {self.waiting}</br>"
        )
            self.station_info.show()
        else:
            self.station_info.hide()
        
    def change_switches_img(self, state):
        if state == Qt.Checked:
            self.switch_png.show()
        else:
            self.switch_png.hide()
            
    def change_occupied_img(self, state):
        if state == Qt.Checked:
            self.occ1_png.show()
            self.occ10_png.show()
        else:
            self.occ1_png.hide()
            self.occ10_png.hide()
        
    def update_block_info_display(self):
        # Always display the block number
        block_number = self.entry_field.text()
        block_info = [f"Block Number: {block_number}"]
        
        #Check possible errors in block entry value   
        if block_number.isdigit() and block_number:
            if block_number:
                block_check = self.check_block_exist(block_number)
                if block_check:
                    #Enable checkboxes if block # entry is valid
                    for checkbox in self.block_info_checkboxes.values():
                        checkbox.setDisabled(False)
                        
                    self.block_info_display.setPlainText("\n".join(block_info))
                    self.block_info_display.show()
                    self.error_label.clear()
                else:
                    #Disable checkboxes if block # entry is not valid
                    for checkbox in self.block_info_checkboxes.values():
                        checkbox.setDisabled(True)
                        
                    self.block_info_display.clear()
                    self.block_info_display.hide()
                    self.error_label.setText(f"Block {block_number} not found.")
        else:
            #Disable checkboxes if block # entry is not valid
            for checkbox in self.block_info_checkboxes.values():
                checkbox.setDisabled(True)
                
            self.block_info_display.clear()
            self.block_info_display.hide()
            self.error_label.setText("Please enter a valid block number.")

        #Check for checkbox selection
        for info, checkbox in self.block_info_checkboxes.items():
            if checkbox.isChecked():
                if info == "Block Length":
                    for data in self.track_data:
                        if data["Block Number"] == int(block_number):
                            block_info.append(f"Block Length: {data['Block Length (m)']} m")
                if info == "Speed Limit":
                    for data in self.track_data:
                        if data["Block Number"] == int(block_number):
                            block_info.append(f"Speed Limit: {data['Speed Limit (Km/Hr)']} Km/Hr")
                if info == "Elevation":
                    for data in self.track_data:
                        if data["Block Number"] == int(block_number):
                            block_info.append(f"Elevation: {data['ELEVATION (M)']} m")
                if info == "Cumulative Elevation":
                    for data in self.track_data:
                        if data["Block Number"] == int(block_number):
                            block_info.append(f"Cumulative Elevation: {data['CUMALTIVE ELEVATION (M)']} m")
                if info == "Block Grade":
                    for data in self.track_data:
                        if data["Block Number"] == int(block_number):
                            block_info.append(f"Block Grade: {data['Block Grade (%)']}%")
                if info == "Allowed Directions of Travel":
                    for data in self.track_data:
                        if data["Block Number"] == int(block_number):
                            block_info.append(f"Allowed Directions of Travel: {self.allowable_directions}")
                if info == "Track Heater":
                    for data in self.track_data:
                        if data["Block Number"] == int(block_number):
                            block_info.append(f"Track Heater: {self.track_heater}")
                if info == "Failures":
                    for data in self.track_data:
                        if data["Block Number"] == int(block_number):
                            block_info.append(f"Failures: {data['Failures']}")
                if info == "Beacon":
                    for data in self.track_data:
                        if data["Block Number"] == int(block_number):
                            block_info.append(f"Beacon: {self.beacon}\n")
        #Then append to display is info is selected
        self.block_info_display.setPlainText("\n".join(block_info))

    def check_block_exist(self, block_number):
        if self.track_data:
            for data in self.track_data:
                if data["Block Number"] == int(block_number):
                    return True
        return False
    
    def add_change_failures_button(self, parent_window):
        self.change_failures_button = QPushButton("Change Failures ->", parent_window)
        self.change_failures_button.setStyleSheet("background-color: red; color: white")
        button_width = 200
        button_height = 30
        button_x = int(950 + (parent_window.width() - 950 - button_width) / 2)
        button_y = parent_window.height() - 50
        self.change_failures_button.setGeometry(button_x, button_y, button_width, button_height)
        self.change_failures_button.setEnabled(False)
        
        self.change_failures_button.clicked.connect(self.show_failure_popup)
    
    def add_tabbar(self, parent_window):
        change_failures_button = QPushButton("Home", parent_window)
        change_failures_button.setStyleSheet("background-color: black; color: white; font-weight: bold; border: 2px solid white; border-bottom: none;")
        change_failures_button.setGeometry(100, 70, 100, 30)
              
        testbench_tab = QPushButton("TestBench", parent_window)
        testbench_tab.setStyleSheet("background-color: black; color: white; font-weight: bold; border: 2px solid white; border-bottom: none;")
        testbench_tab.setGeometry(200, 70, 100, 30)
        
        testbench_tab.clicked.connect(self.show_testbench)
    
    def show_failure_popup(self):
        failure_popup = FailureWindow()
        failure_popup.failure_window.exec()
        
        selected_block = failure_popup.get_selected_block()
        self.failures = failure_popup.get_selected_failures()

        # Update the track_data with failures
        for block in self.track_data:
            if block["Block Number"] == selected_block:
                #Convert to a string for the use of the display, but kept a list privately
                failures_str =  ", ".join(self.failures)
                if self.failures == "None":
                    failures_str = "None"
                block["Failures"] = failures_str
        self.update_block_info_display

    def show_testbench(self):
        testbench_window = TestbenchWindow()
        testbench_window.testbench.exec()
        
class TestbenchWindow():
    speed = ''
    authority = ''
    railway_state = 0
    switch_state = 0
    track_heater_state = 0
    track_state = "Open"
    ticket_sales = ''
    waiting = ''
    light_state = "Green"
    failures = []

    def __init__(self):
        self.testbench = QDialog()
        self.setup_testbench()
        
    def setup_testbench(self):
        self.testbench.setWindowTitle("Change Failures")
        self.testbench.setGeometry(450, 300, 960, 600)
        
        #General layout
        self.add_mta_logo()
        self.add_title()
        self.add_hline()
        
        #Inputs
        self.setup_inputs()
        self.setup_failure_inputs()
        self.add_set_inputs()

        #Outputs
        self.add_outputs()

    def add_mta_logo(self):
        mta_logo = QLabel(self.testbench)
        mta_logo.setGeometry(0, 0, 80, 80)
        mta_logo.setPixmap(QPixmap("src/main/TrackModel/pngs/MTA_logo.png").scaled(80, 80))
        
    def add_title(self):        
        window_width = self.testbench.width()
        label_width = 350
        title_position = int((window_width - label_width) / 2)
        
        title_label = QLabel("Track Model- Testbench", self.testbench)
        title_label.setGeometry(title_position, 25, label_width, 40)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        
    def add_hline(self):
        thickness = 5
        line = QFrame(self.testbench)
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(0, 80, 960, thickness)
        line.setLineWidth(thickness)
        
    def setup_inputs(self):
        blue_background = QWidget(self.testbench)
        blue_background.setGeometry(10, 120, 400, 450)
        blue_background.setStyleSheet("background-color: #A9D0F5;")

        white_background = "background-color: white"

        inputs_label = QLabel("Change Inputs:", blue_background)
        inputs_label.setGeometry(0, 0, 400, 30)
        inputs_label.setStyleSheet("background-color: blue; color: white; font-weight: bold")
        inputs_label.setAlignment(Qt.AlignCenter)

        select_block = QLabel("Select Block #:", blue_background)
        select_block.setGeometry(10, 50, 150, 30)
        self.block_input = QSpinBox(blue_background)
        self.block_input.setGeometry(120, 50, 50, 30)
        self.block_input.setStyleSheet(white_background)
        self.block_input.setMinimum(1)
        self.block_input.setMaximum(15)
        self.block_input.setValue(1)
        go_button = QPushButton("Go", blue_background)
        go_button.setGeometry(220, 50, 150, 30)
        go_button.setStyleSheet("background-color: blue; color: white")
        # Connect the button to the update_block_info_display method
        go_button.clicked.connect(self.update_display)

        speed_label = QLabel("Set Commanded Speed (mph):", blue_background)
        speed_label.setGeometry(10, 90, 200, 30)
        self.speed_input = QLineEdit(blue_background)
        self.speed_input.setGeometry(220, 90, 150, 30)
        self.speed_input.setStyleSheet(white_background)
        self.speed_input.setEnabled(False)

        authority_label = QLabel("Set Authority (blocks):", blue_background)
        authority_label.setGeometry(10, 130, 200, 30)
        self.authority_input = QLineEdit(blue_background)
        self.authority_input.setGeometry(220, 130, 150, 30)
        self.authority_input.setStyleSheet(white_background)
        self.authority_input.setEnabled(False)

        railway_label = QLabel("Set Railway Crossing (0/1):", blue_background)
        railway_label.setGeometry(10, 170, 200, 30)
        self.railway_input = QSpinBox(blue_background)
        self.railway_input.setGeometry(220, 170, 150, 30)
        self.railway_input.setStyleSheet(white_background)
        self.railway_input.setMinimum(0)
        self.railway_input.setMaximum(1)
        self.railway_input.setValue(0)
        self.railway_input.setEnabled(False)

        switch_label = QLabel("Set Switch Position (0/1):", blue_background)
        switch_label.setGeometry(10, 210, 200, 30)
        self.switch_input = QSpinBox(blue_background)
        self.switch_input.setGeometry(220, 210, 150, 30)
        self.switch_input.setStyleSheet(white_background)
        self.switch_input.setMinimum(0)
        self.switch_input.setMaximum(1)
        self.switch_input.setValue(0)
        self.switch_input.setEnabled(False)

        heater_label = QLabel("Set Track Heater (0/1):", blue_background)
        heater_label.setGeometry(10, 250, 200, 30)
        self.heater_input = QSpinBox(blue_background)
        self.heater_input.setGeometry(220, 250, 150, 30)
        self.heater_input.setStyleSheet(white_background)
        self.heater_input.setMinimum(0)
        self.heater_input.setMaximum(1)
        self.heater_input.setValue(0)
        self.heater_input.setEnabled(False)

        track_state_label = QLabel("Set Track State:", blue_background)
        track_state_label.setGeometry(10, 290, 200, 30)
        self.track_open = QRadioButton("Open", blue_background)
        self.track_open.setGeometry(120, 290, 60, 30)
        self.track_open.setEnabled(False)
        self.track_occupied = QRadioButton("Occupied", blue_background)
        self.track_occupied.setGeometry(190, 290, 80, 30)
        self.track_occupied.setEnabled(False)
        self.track_maintenance = QRadioButton("Maintenance", blue_background)
        self.track_maintenance.setGeometry(280, 290, 100, 30)
        self.track_maintenance.setEnabled(False)
        self.track_state_buttons = QButtonGroup()
        self.track_state_buttons.addButton(self.track_open)
        self.track_state_buttons.addButton(self.track_occupied)
        self.track_state_buttons.addButton(self.track_maintenance)
        

        ticket_sales_label = QLabel("Set Ticket Sales/Hr:", blue_background)
        ticket_sales_label.setGeometry(10, 330, 200, 30)
        self.ticket_sales_input = QLineEdit(blue_background)
        self.ticket_sales_input.setGeometry(220, 330, 150, 30)
        self.ticket_sales_input.setStyleSheet(white_background)
        self.ticket_sales_input.setEnabled(False)

        waiting_label = QLabel("Set Waiting @ Station:", blue_background)
        waiting_label.setGeometry(10, 370, 200, 30)
        self.waiting_input = QLineEdit(blue_background)
        self.waiting_input.setGeometry(220, 370, 150, 30)
        self.waiting_input.setStyleSheet(white_background)
        self.waiting_input.setEnabled(False)

        light_label = QLabel("Set Light Color:", blue_background)
        light_label.setGeometry(10, 410, 150, 30)
        self.green_radio = QRadioButton("Green", blue_background)
        self.green_radio.setGeometry(170, 410, 70, 30)
        self.green_radio.setEnabled(False)
        self.yellow_radio = QRadioButton("Yellow", blue_background)
        self.yellow_radio.setGeometry(250, 410, 70, 30)
        self.yellow_radio.setEnabled(False)
        self.red_radio = QRadioButton("Red", blue_background)
        self.red_radio.setGeometry(330, 410, 70, 30)
        self.red_radio.setEnabled(False)
        self.light_state_buttons = QButtonGroup()
        self.light_state_buttons.addButton(self.green_radio)
        self.light_state_buttons.addButton(self.yellow_radio)
        self.light_state_buttons.addButton(self.red_radio)

    def setup_failure_inputs(self):
        red_background = QWidget(self.testbench)
        red_background.setGeometry(500, 120, 350, 80)
        red_background.setStyleSheet("background-color: #ffd6d6;")

        failure_label = QLabel("Set Failure Input:", red_background)
        failure_label.setGeometry(0, 0, 350, 30)
        failure_label.setStyleSheet("background-color: red; color: white; font-weight: bold")
        failure_label.setAlignment(Qt.AlignCenter)

        self.failure_checkboxes = []
        failures = [
            "Track Circuit Failure",
            "Power Failure",
            "Broken Rail"
        ]
        x_offset = 0
        for failure in failures:
            option = QCheckBox(failure, red_background)
            option.setGeometry(x_offset, 40, 150, 30)
            if failure == "Broken Rail":
                option.setGeometry(x_offset-40, 40, 150, 30)
            option.setStyleSheet("background-color: #ffd6d6")
            self.failure_checkboxes.append(option)
            x_offset += 150
    
    def add_set_inputs(self):
        # Create a green button
        self.set_inputs_button = QPushButton("Set Inputs", self.testbench)
        self.set_inputs_button.setGeometry(625, 210, 100, 30)
        self.set_inputs_button.setStyleSheet("background-color: green; color: white; font-weight: bold")
        self.set_inputs_button.setEnabled(False)
        self.set_inputs_button.clicked.connect(self.update_outputs)
            
    def update_display(self):
        self.selected_block = self.block_input.value()
        # self.outputs.setPlainText(f"\nBlock number: {self.selected_block}")
        # Disable all input fields and buttons at the beginning
        self.speed_input.setEnabled(False)
        self.authority_input.setEnabled(False)
        self.railway_input.setEnabled(False)
        self.switch_input.setEnabled(False)
        self.heater_input.setEnabled(False)
        self.ticket_sales_input.setEnabled(False)
        self.waiting_input.setEnabled(False)

        # Reset the radio button state
        self.track_open.setEnabled(False)
        self.track_occupied.setEnabled(False)
        self.track_maintenance.setEnabled(False)

        # Reset the radio button state
        self.green_radio.setEnabled(False)
        self.yellow_radio.setEnabled(False)
        self.red_radio.setEnabled(False)
        # Enable the relevant input fields and buttons based on the selected block
        if self.selected_block == 5:
            self.switch_input.setEnabled(True)
        if self.selected_block == 10 or self.selected_block == 15:
            self.ticket_sales_input.setEnabled(True)
            self.waiting_input.setEnabled(True)

        self.heater_input.setEnabled(True)
        self.speed_input.setEnabled(True)
        self.authority_input.setEnabled(True)
        # Enable the radio buttons for track state and light state
        self.track_open.setEnabled(True)
        self.track_occupied.setEnabled(True)
        self.track_maintenance.setEnabled(True)
        self.green_radio.setEnabled(True)
        self.yellow_radio.setEnabled(True)
        self.red_radio.setEnabled(True)

        # Enable the "Set Inputs" button
        self.set_inputs_button.setEnabled(True)

    def add_outputs(self):
        self.outputs = QTextEdit(self.testbench)
        self.outputs.setGeometry(500, 250, 350, 300)
        self.outputs.setStyleSheet("background-color: white; font-size: 14px")
        self.outputs.setReadOnly(True)
        self.outputs.show()

    def update_outputs(self):
        self.outputs.clear()
        self.failures = []
        self.outputs.append(f"\nBlock Number: {self.selected_block}")
        if self.speed_input.text() != '':
            self.speed = int(self.speed_input.text())
            self.outputs.append(f"Commanded Speed: {self.speed}")
        if self.authority_input.text() != '':
            self.authority = int(self.authority_input.text())
            self.outputs.append(f"Authority: {self.authority}")
        # self.railway_state = self.railway_input.value()
        if self.selected_block == 5:
            self.switch_state = self.switch_input.value()
            self.outputs.append(f"Switch State: {self.switch_state}")
        self.track_heater_state = self.heater_input.value()
        self.outputs.append(f"Track Heater State: {self.track_heater_state}")
        if self.selected_block == 10 or self.selected_block == 15:
            if self.ticket_sales_input.text() != '':
                self.ticket_sales = int(self.ticket_sales_input.text())
                self.outputs.append(f"Authority: {self.ticket_sales}")
            if self.waiting_input.text() != '':
                self.waiting = int(self.waiting_input.text())
                self.outputs.append(f"Authority: {self.waiting}")
        #Check for track state input
        track_state = self.track_state_buttons.checkedButton()
        if track_state:
            self.track_state = track_state.text()
            self.outputs.append(f"Track State: {self.track_state}")
        #Check for light color input
        light_state = self.light_state_buttons.checkedButton()
        if light_state:
            self.light_state = light_state.text()
            self.outputs.append(f"Light State: {self.light_state}")
        #Failures
        for checkbox in self.failure_checkboxes:
            if checkbox.isChecked():
                self.failures.append(checkbox.text())
        self.outputs.append(f"Failures: {self.failures}")

if __name__ == '__main__':
    selection_window = SelectionWindow()
