#USING THE LIBRARY FROM THIS BEAUTIFUL BEAUTIFUL MAN
#https://github.com/almottier/TapoP100

from PyP100 import PyP110

p110 = PyP110.P110("192.168.43.11", "21240797@students.latrobe.edu.au", "3x9gz872")

# The P110 has all the same basic functions as the plugs and additionally allow for energy monitoring.
print("Turning on plug...")
p110.turnOn()
print( p110.getEnergyUsage() )  # Returns dict with all of the energy usage of the connected plug
print("Turning off in 10 seconds...")
p110.turnOffWithDelay(10)

#p110.getEnergyData(1706825847, 1708643847, MeasureInterval.DAYS) # Returns power consumption per day since 1st Feb 24