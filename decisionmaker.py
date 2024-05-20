from metermodule.simulatedmeterclass import SimulatedConsumerMeter
from priority import Device, json_export, json_parse
import os
from flask import *
import threading

class listObject:
    def __init__(self):
        self.devicelist = []

    def append_device(self, i):
        self.devicelist.append(i)

    def get_devices(self):
        return self.devicelist
    
    def remove_device(self, i):
        del self.devicelist[i]

#flask constructor
api = Flask(__name__) 

#load devices from json
print("Initializing system...")

deviceSystem = listObject()

filename = "exported_devices.json"
print(f"Attempting import of devices from {filename}")
templist = json_parse(filename)
deviceSystem.devicelist = templist
print("Devices parsed:")
print( deviceSystem.get_devices() )

#API CALLS
@api.route('/')
def api_test():
    return "API Route works! Hello World! This text is being displayed with a Flask instance running asynchronously within a separate thread!"

@api.route('/success') #generic return success
def success():
    return "Operation complete!"

@api.route('/devices/get', methods=['GET'])
def api_getDevices():
    templist = []
    for i in deviceSystem.get_devices():
        templist.append(i.toJson())
    print(templist)
    return jsonify(templist)

@api.route('/devices/add', methods=['POST'])
def api_addDevices(): #an example request: POST /devices/add?devicename=toaster&deviceconsumption=200&devicestatus=True&devicepriority=2
    devicename = request.args.get("devicename") #should be a string
    deviceconsumption = request.args.get("deviceconsumption") #should be an integer in watts
    devicestatus = request.args.get("devicestatus") #should be either True or False
    devicepriority = request.args.get("devicepriority") #any number from 1 to 5

    if devicename: #check that devicename exists before attempting input
        newDevice = Device(devicename, devicepriority, devicestatus, deviceconsumption)
        deviceSystem.append_device(newDevice)
        return("New device added!: " + devicename)
    else:
        return("Operation failed! Devicename is required!")

@api.route('/devices/remove', methods=['DELETE'])
def api_removeDevice(): #an example request: DELETE /devices/remove?devicename=Toaster

    def linearsearch(list, name):
        #"if word with name is in the list, return its index"
        #"otherwise, return -1"
        for i, Device in enumerate(list):
            if Device.name == name:
                return i
        return -1

    devicename = request.args.get("devicename") #should be a string matching the name of a device in the devicelist

    index = linearsearch(deviceSystem.get_devices(), devicename)

    if index == -1:
        return("No device appears to be in list by that name!")
    else:
        deviceSystem.remove_device(index)
        return("Device removed!")


apiThread = threading.Thread(target=api.run)
apiThread.start() #god i love multithreading

#MAIN LOOP
isRunning = True
while isRunning:
    input("Do a thing!")
    print("Doing a thing!")
    print( deviceSystem.get_devices() )