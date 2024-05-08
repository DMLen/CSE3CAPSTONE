import json
import os

class Device:
    def __init__(self, name, priority, plug_status, energy):
        self.name = name
        self.priority = priority
        self.plug_status = plug_status
        self.energy = energy

class MonitoringSystem:
    def __init__(self):
        self.devices = {}

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

        elif x == ("n"):
            print("Cancelling operation!")
            pass
    
        else:
            print("Invalid input! Cancelling operation!")
            pass

def json_import(file):
    f = open(file, "r")
    #read file contents line by line
    #instantiate device objects based on json dict contents
    #use add_device func for instantiation into the energy monitoring system

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
            filename = "exported_devices.json"
            json_export( monitoring_system.return_list(), filename)

        else:
            print("Invalid choice. Please try again.")
