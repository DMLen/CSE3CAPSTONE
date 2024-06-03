from priority import Device
from PyP100 import PyP110
from time import sleep

ip1 = "192.168.0.225"
ip2 = "192.168.0.226"
emailaddr = "21240797@students.latrobe.edu.au"
passw = "mbw28bag"

testplug1 = Device(ip1, emailaddr, passw, "Lamp", 1)
testplug2 = Device(ip2, emailaddr, passw, "Heater", 1)
#testplug1 = PyP110.P110(ip1, emailaddr, passw)

testplug1.turnOn()
testplug2.turnOn()
sleep(5)
print(f"{testplug1.name} info: {testplug1.returnConsumption()} watts!\n{testplug2.name} info: {testplug2.returnConsumption()} watts!")

print(f"{testplug1.getDeviceInfo()}")
print(f"{testplug2.getDeviceInfo()}")

print(f"{testplug1.getEnergyUsage()}")
print(f"{testplug2.getEnergyUsage()}")

print(f"Plug 1 state: {testplug1.returnState()}")
print(f"Plug 2 state: {testplug2.returnState()}")

print("Turning off!")
testplug1.turnOff()
testplug2.turnOff()
print(f"Plug 1 state: {testplug1.returnState()}")
print(f"Plug 2 state: {testplug2.returnState()}")

print(f"{testplug1.getDeviceInfo()}")
print(f"{testplug2.getDeviceInfo()}")
