from metermodule.simulatedmeterclass import SimulatedConsumerMeter
from priority import Device, json_export, json_parse
import os
from flask import *
import threading
import sys
from datetime import datetime

print("Initialising system...")
class listObject: #this holds our devices and lets us change them dynamically
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

#initialize the system with devices from json
filename = "exported_devices.json"
templist = json_parse(filename)
for i in templist:
    deviceSystem.append_device(i)

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
    deviceIP = request.args.get("deviceIP") #should be a valid ipv4 local address in string format

    overwrittenconsumption = 0
    overwrittenstatus = 0
    overwrittenpriority = 0
    overwrittenIP = 0

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

    if deviceIP:
        (deviceSystem.get_deviceSingle(index)).overwritePlugIP(deviceIP)
        overwrittenIP = 1

    return(f"""Operation complete!\n
            Devicename: {devicename}\n
            Overwritten consumption: {overwrittenconsumption} (if 1; new value is {deviceconsumption})\n
            Overwritten status: {overwrittenstatus} (if 1; new value is {devicestatus})\n
            Overwritten priority: {overwrittenpriority} (if 1; new value is {devicepriority})
            Overwritten IP: {overwrittenIP} (if 1; new value is {deviceIP})
           """) #p.s. can someone fix these newlines not working? the return text looks ugly and messy as they dont work
        

#overwrite device
#get single device
#toggle single device


apiThread = threading.Thread(target=api.run)
apiThread.start() #god i love multithreading

now = datetime.now()
time_date = now.strftime("%H:%M:%S %d/%m/%Y")

#MAIN LOOP
print(f"Program started at {time_date}!")
isRunning = True
while isRunning:
    input("Do a thing!\n") #algorithm will go here btw. this is just so we can make sure the device list is updating properly
    print("Doing a thing!")
    print( deviceSystem.get_devices() )

now = datetime.now()
time_date = now.strftime("%H:%M:%S %d/%m/%Y")
print(f"Program terminated at {time_date}!")