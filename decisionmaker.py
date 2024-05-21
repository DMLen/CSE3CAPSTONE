from metermodule.simulatedmeterclass import SimulatedConsumerMeter
from priority import Device, json_export, json_parse
import os
from flask import *
import threading
import sys

class listObject:
    def __init__(self):
        self.devicelist = []

    def append_device(self, i):
        self.devicelist.append(i)

    def get_devices(self):
        return self.devicelist
    
    def remove_device(self, i):
        del self.devicelist[i]

    def get_deviceSingle(self, i):
        return self.devicelist[i]
        

#flask constructor
api = Flask(__name__) 

deviceSystem = listObject()

filename = "exported_devices.json"

#HELPER FUNCTIONS
def linearsearch(list, name):
        #"if device with name is in the list, return its index"
        #"otherwise, return -1"
        for i, Device in enumerate(list):
            if Device.name == name:
                return i
        return -1

#API CALLS
@api.route('/')
def api_test():
    return "API Route works! Hello World! This text is being displayed with a Flask instance running asynchronously within a separate thread!"

@api.route('/success') #generic return success
def success():
    return "Operation complete!"

#this is a stupid hack. multithreading breaks initializing json devices. it is some voodoo shit i dont understand. just make sure this is called asap whenever the program starts.
@api.route('/devices/load')
def api_devicesLoad():
    templist = json_parse(filename)
    deviceSystem.devicelist = templist
    return "Operation complete!"

@api.route('/devices/get', methods=['GET'])
def api_getDevices():
    templist = deviceSystem.get_devices()
    returnlist = []
    print("Templist: " + str(templist), file=sys.stderr) #debug statement
    for i in templist:
        returnlist.append(i.toJson())
    print("Returnlist: " + str(returnlist), file=sys.stderr)
    return jsonify(returnlist)

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

    devicename = request.args.get("devicename") #should be a string matching the name of a device in the devicelist

    index = linearsearch(deviceSystem.get_devices(), devicename)

    if index == -1:
        return("No device appears to be in list by that name!")
    else:
        deviceSystem.remove_device(index)
        return("Device removed!")
    
#todo: add new api routes
#edit device
@api.route('/devices/edit', methods=['PUT']) #please refer to documentation for proper usage of this method!
def api_editDevice():
    devicename = request.args.get("devicename") #should be a string, required. select the device to be overwritten.
    deviceconsumption = request.args.get("deviceconsumption") #should be an integer in watts. if provided, overwrites the device wattage.
    devicestatus = request.args.get("devicestatus") #should be either True or False. if provided, overwrites the device current state.
    devicepriority = request.args.get("devicepriority") #any number from 1 to 5. if provided, overwrites the device current priority.

    overwrittenconsumption = 0
    overwrittenstatus = 0
    overwrittenpriority = 0

    if not devicename:
        return("Device name is required!")
    
    index = linearsearch(deviceSystem.get_devices(), devicename)
    if index == -1:
        return("No device appears to be in list by that name!")
    
    if deviceconsumption:
        (deviceSystem.get_deviceSingle(index)).overwriteConsumption(deviceconsumption)
        overwrittenconsumption = 1

    if devicestatus:
        (deviceSystem.get_deviceSingle(index)).overwriteState(devicestatus)
        overwrittenstatus = 1

    if devicepriority:
        (deviceSystem.get_deviceSingle(index)).overwritePriority(devicepriority)
        overwrittenpriority = 1

    return(f"""Operation complete!\n
            Devicename: {devicename}\n
            Overwritten consumption: {overwrittenconsumption} (if 1; new value is {deviceconsumption})\n
            Overwritten status: {overwrittenstatus} (if 1; new value is {devicestatus})\n
            Overwritten priority: {overwrittenpriority} (if 1; new value is {devicepriority})
           """)
        

#overwrite device
#get single device
#toggle single device


apiThread = threading.Thread(target=api.run)
apiThread.start() #god i love multithreading

#MAIN LOOP
isRunning = True
while isRunning:
    input("Do a thing!\n")
    print("Doing a thing!")
    print( deviceSystem.get_devices() )