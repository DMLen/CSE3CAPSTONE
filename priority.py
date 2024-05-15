import json
import os

class Device:
    def __init__(self, name, priority, plug_status, energy):
        self.name = name
        self.priority = priority
        self.plug_status = plug_status
        self.energy = energy

    def __str__(self):
        #object print method
        return f"This device's name is '{self.name}'. The current priority is '{self.priority}', the plug status is currently '{self.plug_status}', and the current energy consumption is '{self.energy}'."
    
    def __repr__(self):
        #more readable representation method (for json import)
        return f"Device object '{self.name}' at {hex(id(self))}"

class MonitoringSystem:
    def __init__(self):
        self.devices = {} #wouldnt it be better for this to be a list populated with objects of the Device class we just specified, instead of a dictionary?

    def add_device(self, name, priority):
        if name in self.devices:
            print(f"Device '{name}' already exists. Please choose a different name.")
            return
        plug_status = input(f"Do you want to turn on the plug for device '{name}'? (yes/no): ")
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

# Example usage
if __name__ == "__main__":
    monitoring_system = MonitoringSystem()

    while True:
        print("\n1. Add Device")
        print("2. Set Priority")
        print("3. Turn On/Off Plug")
        print("4. List Devices")
        print("5. Exit")
        print("6. Export data to JSON")
        print("7. Import data from JSON")

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

                    

        else:
            print("Invalid choice. Please try again.")
