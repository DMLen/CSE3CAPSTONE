class SimulatedConsumerMeter:
    #this is a simulation of a consumer power meter, created so we can still test and implement our product software despite the very real possibility of not acquiring hardware within the project timeframe.
    #we assume pv (photovoltaic power production) default wattage to be 5kW, and power consumption of the house to be 1.2kW
    #all power values are in Watts, and represent the current wattage of the (imaginary) components at the time of calling.
    def __init__(self):
        self.powerConsumption = 1200
        self.pvPower = 5000
        
    def get_powerConsumption(self):
            return self.powerConsumption
        
    def get_pvPower(self):
            return self.pvPower
        
    #if powerDifference returns a negative integer (default -800), power is in defecit to the household.
    #if powerDifference returns a positive integer, power is in excess and is being exported to the grid.        
    def get_powerDifference(self):
        return self.pvPower - self.powerConsumption
    
    def set_powerConsumption(self, value):
        self.powerConsumption = value

    def set_pvPower(self, value):
        self.pvPower = value

    def get_status(self):
        if (self.pvPower - self.powerConsumption) < 0:
             return "defecit"
        else:
             return "surplus"
    
    #print out relevant information about the powerbox in its current state
    def print_readout(self):
        print("Current consumption: " + str(self.powerConsumption) )
        print("Current PV power: " + str(self.pvPower) )
        print("Current raw surplus/defecit: " + str(self.get_powerDifference()) )
        print("Status: " + self.get_status())