import tkinter
from tkinter import filedialog
import math, time
import serial
import pynmea2 
from i2clibraries import i2c_hmc5883l


class ROBOT():
    def __init__(self):
        self.lat = 0.0
        self.lng = 0.0
        self.headingDeg = 0
        self.headingMin = 0

        port="/dev/serial0"
        self.ser=serial.Serial(port, baudrate=9600, timeout=0.5) 
        dataout =pynmea2.NMEAStreamReader()
        self.hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
        self.hmc5883l.setContinuousMode()
        self.hmc5883l.setDeclination(2,25)

    def getGPSData(self):
        newdata=self.ser.readline()
        #print(newdata)
        if newdata[0:6] == "$GPRMC":  
            newmsg=pynmea2.parse(newdata)  
            self.lat=newmsg.latitude 
            self.lng=newmsg.longitude 
            gps = "Latitude=" + str(self.lat) + "and Longitude=" +str(self.lng) 
            print(gps)

    def getGPSHeading(self):
        self.headingDeg, self.headingMin = self.hmc5883l.getHeading()
        print(str(self.headingDeg) + " deg, " + str(self.headingMin) + " minutes")

    def distanceFromCoordinates(self, lat1, long1, lat2, long2):
        radius=6371 # radius of earth
        # converion to radians
        lat1=lat1*math.pi/180
        lat2=lat2*math.pi/180
        lon1=long1*math.pi/180
        lon2=long2*math.pi/180

        deltaLat=lat2-lat1
        deltaLon=lon2-lon1

        a=math.sin((deltaLat)/2)^2 + math.cos(lat1)*math.cos(lat2) * math.sin(deltaLon/2)^2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        return radius*c    #Haversine distance

    def angleFromCoordinate(self, lat1, long1, lat2, long2):
        dLon = (long2 - long1)
        y = math.sin(dLon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
        brng = math.atan2(y, x)
        brng = math.degrees(brng)
        brng = (brng + 360) % 360
        brng = 360 - brng # count degrees clockwise - remove to make counter-clockwise
        return brng

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.input_type = tkinter.IntVar()
        self.input_type.set(0)

        # Input Side
        latlbl_i = tkinter.Label(window, text="Latitude:")
        longlbl_i = tkinter.Label(window, text="Longitude:")
        setlbl = tkinter.Label(window, text="Set Coordinates:")
        getlbl = tkinter.Label(window, text="General Status:")
        cord_listlbl = tkinter.Label(window, text="Coordinates List:")
        self.cord_list = tkinter.Text(window, state='disabled', width=10, height=5)
        self.lat_input = tkinter.Entry(window)
        self.long_input = tkinter.Entry(window)
        self.btn_open_map=tkinter.Button(window, text="Open Map", width=10, command=self.open_map)
        self.btn_add_manual = tkinter.Button(window, text="Add", width=10, command=self.add_manual)
        self.btn_start_robot=tkinter.Button(window, text="START", width=10, command=self.open_map)
        self.btn_stop_robot = tkinter.Button(window, text="STOP", width=10, command=self.add_manual)
        radio_open_map = tkinter.Radiobutton(window, 
                                        text='Select on Map',
                                        padx = 20, 
                                        variable=self.input_type, 
                                        value=0
                                        )

        radio_manual = tkinter.Radiobutton(window, 
                                        text='Manual Selection',
                                        padx = 20, 
                                        variable=self.input_type, 
                                        value=1
                                        )

        # Output Side
        current_loclbl_o = tkinter.Label(window, text="Current Location:")
        latlbl_o = tkinter.Label(window, text="Latitude:")
        longlbl_o = tkinter.Label(window, text="Longitude:")
        speedlbl_o = tkinter.Label(window, text="Speed:")
        self.lat_output = tkinter.Text(window, state='disabled', width=10, height=1)
        self.long_output = tkinter.Text(window, state='disabled', width=10, height=1)
        self.speed_output = tkinter.Text(window, state='disabled', width=10, height=1)

        #input side grid
        
        setlbl.grid(column=0, row=0, sticky='NSWE')
        radio_open_map.grid(column=1, row=1, sticky='NSW')
        radio_manual.grid(column=1, row=2, sticky='NSW')
        self.btn_open_map.grid(column=2, row=1, sticky='NS')
        self.btn_add_manual.grid(column=3, row=4, sticky='NS')
        latlbl_i.grid(column=2, row=2)
        longlbl_i.grid(column=2, row=3, sticky='NSWE')
        self.long_input.grid(column=3, row=2, sticky='NSWE')
        self.lat_input.grid(column=3, row=3, sticky='NSWE')
        self.cord_list.grid(column=1, row=9, sticky='NSWE')
        cord_listlbl.grid(column=0, row=8, sticky='NSWE')

        #output side grid
        getlbl.grid(column=4, row=0, sticky='NSW')
        self.lat_output.grid(column=6, row=3, sticky='NSWE')
        self.long_output.grid(column=7, row=3, sticky='NSWE')
        self.speed_output.grid(column=6, row=4, sticky='NSWE')
        current_loclbl_o.grid(column=5, row=3, sticky='NSW')
        latlbl_o.grid(column=6, row=2, sticky='NSWE')
        longlbl_o.grid(column=7, row=2, sticky='NSWE')
        speedlbl_o.grid(column=5, row=4, sticky='NSW')
        self.btn_start_robot.grid(column=2, row=10, sticky='NS')
        self.btn_stop_robot.grid(column=4, row=10, sticky='NS')
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
        self.window.mainloop()


    def open_map(self):
        pass

    def add_manual(self):
        pass

    def update(self):

        self.window.after(self.delay, self.update)


# Create a window and pass it to the Application object
App(tkinter.Tk(), "RPi_GSM_Robot")