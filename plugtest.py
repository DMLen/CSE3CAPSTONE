from priority import Device
from PyP100 import PyP110

ip1 = "192.168.0.225"
emailaddr = "21240797@students.latrobe.edu.au"
passw = "mbw28bag"

testplug1 = Device(ip1, emailaddr, passw, "Plug 1", 1)
#testplug1 = PyP110.P110(ip1, emailaddr, passw)

testplug1.turnOn()
testplug1.turnOffWithDelay(5)
