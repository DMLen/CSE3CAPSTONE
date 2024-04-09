from simulatedmeterclass import SimulatedConsumerMeter
import threading
from random import randint
import time


#this is a demonstration of the SimulatedConsumerMeter class.
#it accepts no arguments when it is instantiated. it is already instantiated with average values.
#defaults: consumption = 1.2kW, production = 5kW
#all returned integers are in watts.
#1000 watts = 1kw

virtualmeter = SimulatedConsumerMeter()

virtualmeter.print_readout()

#if get_powerDifference returns a negative integer, power is in defecit to the household. we are using more power than we are producing and having to import from the grid (we want to avoid this)
#if a positive integer, power is in surplus and is being exported to the grid. we are producing more power than we are using

print("\nRedefining values so we are in a power defecit")

#using setter methods to change the simulated meter object. these exist for testing purposes.
#in a real power meter, the current consumption and power will depend on appliances and the weather
#in this case, we are now producing less power than we are using
virtualmeter.set_pvPower(800)

virtualmeter.print_readout()

#demonstration of power randomization:
#we can use threading to randomly change the variables of virtualmeter object every 10 seconds
#this is intended for testing other software components relying on the power readings
#something like this would also be useful for testing software components that require a collected history of power readings

#arguments for randomization
maxConsumptionLimit = 2000
minConsumptionLimit = 500

maxProductionLimit = 5000
minProductionLimit = 0

randomizerPeriod = 10 #seconds between randomization
randomizerAmount = 100 #how many times should we randomize

#the code in randomizer() will be run every x seconds (from time.sleep function with randomizerPeriod as arg) 
#it will run y amount of times (from randomizerAmount)
def randomizer():
    for i in range(randomizerAmount):
        val = randint(minProductionLimit, maxProductionLimit) #generate a random integer between these two limits
        virtualmeter.set_pvPower(val)

        val = randint(minConsumptionLimit, maxConsumptionLimit)
        virtualmeter.set_powerConsumption(val)

        print("\nRandomized values: Taking reading " + str(i) + " of " + str(randomizerAmount) + " (polling every " + str(randomizerPeriod) + " seconds)")
        virtualmeter.print_readout()
        time.sleep(randomizerPeriod)

#create thread with target as randomizer() and then start thread
randomizerThread = threading.Thread(target=randomizer)
randomizerThread.start()



