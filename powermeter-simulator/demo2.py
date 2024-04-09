from simulatedmeterclass import SimulatedConsumerMeter
import threading
from random import randint
import time
import math
import numpy as np

#this is a demonstration of the SimulatedConsumerMeter class that leverages a mathematical curve function to randomize pvpower value.
#for simplicity i added new print_readout() function.
#numpy library is required!

virtualmeter = SimulatedConsumerMeter()


print("\nDefault class values of the power meter (household average)")
virtualmeter.print_readout()

#modified "randomizer" is below
#in this file, we show a basic model of daylight where the power production is based off of a sine curve throughout the day
#power production is 0 at the morning, and increases in a curved fashion as a function of time. it peaks at midday, and is zero at sunset and through the night.
#this is very similar to demo1.py with randomization

maximumPower = 5000
randomizerPeriod = 10 #how long in second between repetitions

#following codesnippet is from Voy at stackoverflow
cycles = 2 #how many sine cycles or "days" do we want?
resolution = 25 #how many data points should we generate?

length = np.pi * 2 * cycles
sine_wave = np.sin(np.arange(0, length, length / resolution))
print("\nSine func points: ")
print(sine_wave)

#this produces an array of integers based on a sine function.
#0, 0.481, 0.844, 0.998, 0.904, etc etc...
#all negative numbers will be set to zero so this acts as a list of multiplicative factors
sunlight_factor = []

for i in sine_wave:
    if i > 0:
        sunlight_factor.append(i)
    else:
        sunlight_factor.append(0)

print("\nSunlight factors: ")
print(sunlight_factor)

#"randomizer" function (not actually random)
def randomizer():
    for i in range(resolution):
        power_value = maximumPower * sunlight_factor[i]
        virtualmeter.set_pvPower(power_value)
        
        print("\nRandomized values (solar sine variance): Taking reading " + str(i) + " of " + str(resolution) + " (polling every " + str(randomizerPeriod) + " seconds)")
        virtualmeter.print_readout()
        print("Power production reduced from " + str(maximumPower) + " to " + str(virtualmeter.get_pvPower()) + " based on a sunlight factor of " + str(sunlight_factor[i]) )
        time.sleep(randomizerPeriod)

randomizer()
        











#create thread with target as randomizer() and then start thread
#randomizerThread = threading.Thread(target=randomizer)
#randomizerThread.start()






