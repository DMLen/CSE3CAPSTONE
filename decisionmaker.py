from metermodule.simulatedmeterclass import SimulatedConsumerMeter
from priority import Device, json_export, json_parse
import os
from flask import *
import threading
import sys
from datetime import datetime
import time
import random

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

#creating list holder
deviceSystem = listObject()

#creating virtual powerbox for testing purposes
powerBox = SimulatedConsumerMeter()

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

### CONFIGURATION ###

#polling length (how long should we wait before running the algorithm again)
polling = 30

#randomization range (the upper and lower bounds of power production test values)
maxProductionLimit = 5000
minProductionLimit = 0

### END CONFIGURATION

apiThread = threading.Thread(target=api.run)
apiThread.start() #god i love multithreading
time.sleep(5) #give flask some time to start

now = datetime.now()
time_date = now.strftime("%H:%M:%S %d/%m/%Y")

#MAIN LOOP
print(f"Program started at {time_date}!")
isRunning = True
while isRunning:
    #step 1. assess current system state (consumption)
    #this is written using a non-functional virtual test method for the device objects. (doesnt interface with plugs currently)
    #to make this work, first associate each device object with a physical plug using the interface library in plug_controller.py
    #then, have tempsum be the real current consumption values from all devices that are turned on
    print("Assessing power consumption (virtual simulation):")
    tempsum = 0
    for device in deviceSystem.devicelist:
        if ( int(device.returnState()) == 1 ) or (device.returnState == "1"): #only consider the values of devices we know to be on
            tempsum += device.returnConsumption()
        else:
            pass
    powerBox.set_powerConsumption(tempsum)    
    

    #step 1.2. assess the current system state (production)
    #in a proper implementation, this would be "get production value from the solar panels"
    #we are instead going to use a randomized method to generate these values instead for the purposes of testing (like in demo1.py)
    #obviously you can replace this when properly implementing this.
    production = random.randint(minProductionLimit, maxProductionLimit)
    powerBox.set_pvPower(production)

    #at this state, we know the current consumption of the system, and the production of the system.
    print("!!! CURRENT SYSTEM STATE!!!")
    powerBox.print_readout()
    print("\n") #for prettier printing of following processes

    #If we are currently in a defecit, begin this logic loop to try and minimize the defecit (switching off devices)
    if powerBox.get_status() == "defecit":
        print(f"DEFECIT OF {powerBox.get_powerDifference()}!!! Attempting to minimize it...")

        #priority 1 devices will be considered first for elimination (being turned off)
        #after turning a device off, we then check if there is still a defecit.
        #if there is, we continue.
        #after all priority 1 devices have been turned off, we then begin to consider priority 2 devices.
        #we will do this up to priority 5.

        for priority in range(1, 6): #6 and not 5 because of how range works
            print(f"Considering priority {priority} devices for turning off:")
            for device in deviceSystem.get_devices():
                if ( int(device.priority) == priority ) and ( powerBox.get_status() == "defecit" ): #check if we are considering devices of this priority, and if we are currently in a defecit
                    if int(device.plug_status) == 1: #if device is already on
                        print(f"Turning off {device.name} with a consumption of {device.energy}! Priority: {device.priority}")
                        device.turnOff()

                        #updating consumption of the virtual powerbox
                        #again this wouldnt be needed for a real powerbox.
                        powerBox.powerConsumption -= device.energy

                        print(f"New defecit: {powerBox.get_powerDifference()}\n")

        print("Defecit has been minimized as best we can!")
        powerBox.print_readout()

    #if we are not in a defecit, turn on some devices as long as it wont result in a defecit
    #priority 5 devices we will try to turn on first
    #this is basically the same thing as above but in reverse
    else:
        print(f"SURPLUS OF {powerBox.get_powerDifference()}!!! Let's turn some more devices back on now...")
        for priority in reversed( range(1, 6) ): #outputs the list [5, 4, 3, 2 , 1] and these are the priorities we check in that order
            print(f"Considering priority {priority} devices for turning on:")
            for device in deviceSystem.get_devices():
                if ( int(device.priority) == priority ) and ( powerBox.get_status() == "surplus" ): #if we are currently considering devices of this priority and we are in a surplus, proceed
                    if int(device.plug_status) == 0:
                        print(f"Turning on {device.name} with a consumption of {device.energy}! Priority: {priority}\n")
                        device.turnOn()

                        #updating consumption of the virtual powerbox
                        powerBox.powerConsumption += device.energy
                        print(f"New surplus: {powerBox.get_powerDifference()}\n")

        print("We've tried turning on some devices!")
        powerBox.print_readout()



    #end of algorithm, sleep for length of polling period
    print(f"End of polling activity. Sleeping for {polling} seconds as defined in the config before we repeat!")
    time.sleep(polling)



#POST-LOOP
now = datetime.now()
time_date = now.strftime("%H:%M:%S %d/%m/%Y")
print(f"Program terminated at {time_date}!")