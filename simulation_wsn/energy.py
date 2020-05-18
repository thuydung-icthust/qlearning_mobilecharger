from argparse import ArgumentParser
import numpy as np
from sensor import Sensor



class energy():
    def __init__(self,args, sensorObject):
        self.hyper_lambda = float(args.hyper_lambda)
        self.hyper_beta = float(args.hyper_beta)
        self.__sensorObject = sensorObject

    def energy_receive(self, x_D, y_D):
        received = self.hyper_lambda / (np.sqrt((self.__sensorObject.x_axis - x_D)**2 +(self.__sensorObject.y_axis - y_D)**2) + self.hyper_beta)**2
        return received
    def energy_change_in_time(self, time, x_D, y_D):
        change = (self.energy_receive(x_D, y_D) - self.__sensorObject.avg_consume_energy)*time
        return change
    def update_energy(self, delta_energy):
        self.__sensorObject.remain_energy = self.__sensorObject.remain_energy + delta_energy
    def mc_moving(self, x_D, y_D):
        print("Initial energy of sensor 1 is: {}\n".format(self.__sensorObject.remain_energy))
        print("After: \n")
        change = self.energy_change_in_time(0.5, x_D, y_D)
        self.update_energy(change)
        print("Final energy of sensor 1 is: {}\n".format(self.__sensorObject.remain_energy))
        
def arg_parse():
    parser = ArgumentParser()
    parser.add_argument("--hyper_lambda", help="lambda in energy receive formula", default=40)
    parser.add_argument("--hyper_beta", help="beta in energy receive formula", default=0.4)  
    return parser.parse_args()

if __name__ == '__main__':
    args = arg_parse() # get hyper-parameters
    sensor1 = Sensor(1,1, 20, 1.2)
    energy_ss1 = energy(args, sensor1)

    
    print("Testing Model")
    energy_ss1.mc_moving(0,0)
   