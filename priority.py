import json
import os
from flask import *
import threading
from PyP100 import PyP110

#flask constructor
priorityAPI = Flask(__name__) 

class Device(PyP110.P110):
    def __init__(self, plugip, accountemail, accountpassword, name, priority,):
        super().__init__(plugip, accountemail, accountpassword)
        self.name = name
        self.priority = priority
        self.plug_status = "OBSOLETED"
        self.energy = "OBSOLETED"

    #we inherit some very important functions from the PyP110 class
    #namely, 
    # p110.getEnergyUsage()
    # p100.turnOn()
    # p100.toggleState()
    # p100.getDeviceInfo()
    # (these methods are now called with Device.turnOn(), etc as they are inherited)

    def __str__(self):
        #object print method
        return f"This device's name is '{self.name}'. The current priority is '{self.priority}', the plug status is currently '{self.plug_status}', and the current energy consumption is '{self.energy}'."
    
    def __repr__(self):
        #more readable representation method (for json import)
        return f"Device object '{self.name}' at {hex(id(self))}"
    
    def toJson(self):
        return json.dumps(self.__dict__,)

    def overwritePriority(self, priority):
        self.priority = priority

    def overwritePlugIP(self, ipaddress):
        self.plugip = ipaddress
    
    def returnPlugIP(self):
        return self.plugip
    
    def returnConsumption(self): #redundant? not exactly. the default getDeviceInfo() method returns a dictionary with lots of other info. this function returns only the instantaneous wattage.
        plugdict = self.getEnergyUsage()
        milliwatts = plugdict["current_power"]
        wattage = milliwatts/1000
        return wattage

    
    def returnState(self):
        plugdict = self.getDeviceInfo()
        state = plugdict["device_on"]
        return state
    
    def returnPriority(self):
        return self.priority

class MonitoringSystem:
    def __init__(self):
        self.devices = {} #wouldnt it be better for this to be a list populated with objects of the Device class we just specified, instead of a dictionary?

    def add_device(self, name, priority):
        if name in self.devices:
            print(f"Device '{name}' already exists. Please choose a different name.")
            return
        plug_status = input(f"Do you want to turn on the plug for device '{name}'? (1/0): ")
        energy = float(input(f"Enter energy consumption for device '{name}' (in watts): "))
        self.devices[name] = Device(name, priority, plug_status, energy)
        print(f"Device '{name}' added with priority '{priority}', plug status '{plug_status}', and energy consumption '{energy}' watts.")

    def set_priority(self, name, priority):
        if name not in self.devices:
            print(f"Device '{name}' does not exist.")
            return
        self.devices[name].priority = priority
        print(f"Priority of device '{name}' set to '{priority}'.")

    def turn_on_off_plug(self, name, plug_status):
        if name not in self.devices:
            print(f"Device '{name}' does not exist.")
            return
        self.devices[name].plug_status = plug_status
        print(f"Plug status of device '{name}' set to '{plug_status}'.")

    def list_devices(self):
        print("List of Devices:")
        for device in self.devices.values():
            print(f"Name: {device.name}, Priority: {device.priority}, Plug Status: {device.plug_status}, Energy Consumption: {device.energy} watts")

    def return_list(self):
        return self.devices.values()

def json_export(list, file):
    if not os.path.exists(file): #check file doesnt already exist first to prevent accidental overwrite
        f = open(file, "w")
        for device in list:
            jsondata = json.dumps(device.__dict__) #convert each object into a json dictionary
            print("Device Object" + jsondata)
            f.write(jsondata + "\n") #write each object to a newline in json
        f.close()
        print("Export complete! Please find saved data at " + file)

    else: #this runs if the first condition (file not already existing) fails
        print("File already exists!")
        x = input("Do you wish to overwrite? (y to overwrite, n to cancel operation): ")
        if x == ("y"):
            print("Overwriting json!")

            #this is the same write code as above, but it is only called to overwrite whatever is already in file!
            f = open(file, "w")
            for device in list:
                jsondata = json.dumps(device.__dict__) #convert each object into a json dictionary
                print("Device Object" + jsondata)
                f.write(jsondata + "\n") #write each object to a newline in json
            f.close()
            print("Export complete! Please find saved data at " + file)
    
        else:
            print("Cancelling operation!")
            pass

#these json methods arent part of the energymonitoring system class so they will have to be exported separately
def json_parse(file):
    if not os.path.exists(file):
        print("File doesn't exist! Cancelling operation!") #prevent errors if a json file doesnt exist at provided directory
        return -1
    else:
        device_list = []
        print("Parsing device objects from json data!")
        counter = 0
        f = open(file, "r")
        lines = f.readlines()
        for line in lines: #read file contents line by line
            print("Instantiating object " + str(counter) )
            device_dictionary = json.loads(line) #may cause crashes if the json isn't structured appropriately, untested. device_dictionary holds current line contents.
            print( str(device_dictionary) )

            #instantiate device objects based on json dict contents
            name = 'device_{}'.format(counter) 
            name = Device(**device_dictionary) #instantiate each json dictionary as device argument. multiple parameters are passed at once. it just works
            print(name) #print object to verify attributes are set correctly

            device_list.append(name) #append device object to the return list
            counter += 1

        f.close()
        print("Device object creation complete! " + str(counter) + " objects created!")
        return device_list

#constructor for energy system
monitoring_system = MonitoringSystem()

#priorityAPI functions below
@priorityAPI.route('/')
def priorityAPI_test():
    return "priorityAPI Route works! Hello World! This text is being displayed with a Flask instance running asynchronously within a separate thread!"

@priorityAPI.route('/success') #generic return success
def success():
    return "Operation complete!"

@priorityAPI.route('/devices/get', methods=['GET'])
def priorityAPI_getDevices():
    #now the dictionary implementation is really painful
    #we cannot directly export a dictionary of values. if it was a list of objects then we wouldn't have to do this badness.
    #no good! too bad! this is a hack but it works and that is all that matters
    dict = monitoring_system.return_list()
    templist = []
    for i in dict:
        templist.append(i.toJson())
    return jsonify(templist)

@priorityAPI.route('/devices/add', methods=['POST'])
def priorityAPI_addDevices(): #an example request: POST /devices/add?devicename=toaster&deviceconsumption=200&devicestatus=on&devicepriority=2
    devicename = request.args.get("devicename")
    deviceconsumption = request.args.get("deviceconsumption")
    devicestatus = request.args.get("devicestatus")
    devicepriority = request.args.get("devicepriority")

    if devicename: #check that devicename exists before attempting input
        newDevice = Device(devicename, devicepriority, devicestatus, deviceconsumption)
        monitoring_system.devices[devicename] = newDevice
        return("New device added!: " + devicename)
    else:
        return("Operation failed! Devicename is required!")



#program main loop
#priorityAPIThread = threading.Thread(target=priorityAPI.run)
#priorityAPIThread.start() #god i love multithreading
if __name__ == "__main__":

    while True:
        print("\n1. Add Device")
        print("2. Set Priority")
        print("3. Turn On/Off Plug")
        print("4. List Devices")
        print("5. Exit")
        print("6. Export data to local JSON")
        print("7. Import data from local JSON")
        print("8. [DEBUG] View returned list")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter device name: ")
            priority = input("Enter priority (priority 1, priority 2, priority 3): ")
            monitoring_system.add_device(name, priority)
        elif choice == "2":
            name = input("Enter device name: ")
            priority = input("Enter new priority (priority 1, priority 2, priority 3): ")
            monitoring_system.set_priority(name, priority)
        elif choice == "3":
            name = input("Enter device name: ")
            plug_status = input("Turn on or off plug? (on/off): ")
            monitoring_system.turn_on_off_plug(name, plug_status)
        elif choice == "4":
            monitoring_system.list_devices()
        elif choice == "5":
            print("Exiting...")
            break
        elif choice == "6":
            print("Export data to JSON...")
            filename = "exported_devices.json" #changing filename here changes the destination of export data
            json_export( monitoring_system.return_list(), filename)
        elif choice == "7":
            print("Import data from JSON...")
            filename = "exported_devices.json" #changing filename here changes the target of import data
            if json_parse(filename) != -1:
                devicelist = json_parse(filename) #this function returns a dictionary of device objects created from json data
                print("Parsed objects: " + str(devicelist) ) #verify that returned objects are correct
                for device in devicelist:
                    monitoring_system.devices[device.name] = Device(device.name, device.priority, device.plug_status, device.energy) #add new entry to the monitored device list as dictionary entries
                    #words dont exist for how much i dont like this implementation
            else:
                print("Import failed!")

        elif choice == "8": #delete this later
            returned = monitoring_system.return_list()
            print(returned)
                    

        else:
            print("Invalid choice. Please try again.")
