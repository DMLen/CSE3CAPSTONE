class Device:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

class MonitoringSystem:
    def __init__(self):
        self.devices = {}

    def add_device(self, name, priority):
        if name in self.devices:
            print(f"Device '{name}' already exists. Please choose a different name.")
            return
        self.devices[name] = Device(name, priority)
        print(f"Device '{name}' added with priority '{priority}'.")

    def set_priority(self, name, priority):
        if name not in self.devices:
            print(f"Device '{name}' does not exist.")
            return
        self.devices[name].priority = priority
        print(f"Priority of device '{name}' set to '{priority}'.")

    def list_devices(self):
        print("List of Devices:")
        for device in self.devices.values():
            print(f"Name: {device.name}, Priority: {device.priority}")


# Example usage
if __name__ == "__main__":
    monitoring_system = MonitoringSystem()

    while True:
        print("\n1. Add Device")
        print("2. Set Priority")
        print("3. List Devices")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter device name: ")
            priority = input("Enter priority (low, medium, high): ")
            monitoring_system.add_device(name, priority)
        elif choice == "2":
            name = input("Enter device name: ")
            priority = input("Enter new priority (low, medium, high): ")
            monitoring_system.set_priority(name, priority)
        elif choice == "3":
            monitoring_system.list_devices()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
