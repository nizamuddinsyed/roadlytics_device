

#################################################################################################################################
#                                                                                                                               #
#                                                                                                                               #
#          This code belongs to project roadlytics - lsbg hamburg, usage of this source code should be authorized by Roadlytics # 
#          changes/modification/code-reuse should be informed immediately to team Roadlytics.                                   #
#          Organisation    :   Landesbetrieb Straßen, Brücken und Gewässer, hamburg                                             #
#          email           :   nizamuddin.syed@lsbg.hamburg.de                                                                  #
#                                                                                                                               #
#                                                                                                                               #
#################################################################################################################################



# The main purpose of this code is to establish serial communication with all the hardware modules of the devices
# parse the raw NMEA sentences and store the data locally into time specific directories and log the error if it encounters during the process.



# Below are the packages used in the script

import io                   # default interface to access files and streams
import json                 # built-in python package called json, which can be used to work with JSON data.
import pynmea2              # package to parse raw nmea sentences 
import serial               # package to work with serial ports, cases: /dev/ttyAMA0 or /Serial0 /USB0 or COM ports
import datetime             # package for manipulating date and time    
from pathlib import Path    # package to handle file system paths

# stores the current date time of the system, whenever the device turns ON, a directory is created with the system datetime
currentTime = datetime.datetime.now()

# Creates a new directory if it doesn't exist already and creates folders with timestamp for every session
foldername = "/home/pi/Desktop/Data_GNSS/" + str(currentTime.date()) + "/" # folder structure
Path(foldername).mkdir(parents=True, exist_ok=True) 
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=5.0) # estblashing serial connection with Baudrate 9600
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))    # to READ or WRITE data 'TO' and 'FROM' the file 
print(sio.readline())                                  # prints all NMEA sentences on the console
time =  str(currentTime.hour) + str(currentTime.minute) + str(currentTime.second) # system time
pushRawData= open(foldername + "rawData_"+ time + ".log","w+")  # all the RAW NMEA sentences will be stored at this location
pushGgaData= open(foldername + "ggaData_"+ time + ".txt","w+")  # all the GGA messages will be stored at this location
pushRmcData= open(foldername + "rmcData_"+ time + ".txt","w+")  # all the RMC messages will be stored at this location
datagga =[]         # empty collection for GGA specific data
datarmc =[]         # empty collection for RMC specific data
knots_to_Kmph = 1.852
while 1:
    try:
        line = sio.readline()           # reads until new line or EOF
        print(line)                     # printing the above read line, just for validation
        print("------------>")
        msg = pynmea2.parse(line)       # Parses a string representing a NMEA 0183 sentence, and returns a NMEASentence object
        print(repr(msg))                # Return the canonical string representation of the object.
        pushRawData.write(line + "\n")  # writing RAW data into a file 
        # pushRawData.write()
        if isinstance(msg, pynmea2.types.talker.GGA):
            print(repr(msg))
            # pushGgaData.write(repr(msg) + "\n")
            latlonggga = {"latitude": msg.latitude, "longitude": msg.longitude}
            json.dump(latlonggga, pushGgaData)
            pushGgaData.write(",")                  # writing GGA {latitude,, longitude} into a file
        if isinstance(msg, pynmea2.types.talker.RMC):
            print(repr(msg))
            latlongrmc = {"latitude": msg.latitude, "longitude": msg.longitude, "speed": float(msg.spd_over_grnd*knots_to_Kmph), "date":str(msg.datestamp), "timestamp": str(msg.timestamp), "status": msg.status}
            json.dump(latlongrmc, pushRmcData)
            pushRmcData.write(",")                   # writing RMC {latitude,longitude, speed, date, timestamp...} into a file

# exception/error handling
    
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue