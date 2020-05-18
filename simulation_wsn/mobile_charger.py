from sensor import Sensor
from argparse import ArgumentParser
import numpy as np
import random

class Point():
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
    def dist_2points(self, point2):
        dis = np.sqrt((self.x - point2.x)**2 +(self.y - point2.y)**2)
        return dis
    

class mobileCharger():
    def __init__(self, velocity, cur_point):
        #self.hyper_lambda = args.hyper_lambda
        #self.hyper_beta = args.hyper_beta
        self.velocity = velocity
        self.cur_point = cur_point
        self.remain_MC_energy = 30000
        self.minumum_e = 0.2*300
        #self.next_point = Point(0,0)

    def moving_to(self, next_point, all_sensors):
        dis = self.cur_point.dist_2points(next_point)
        time_moving = dis/ self.velocity
        for sensor in all_sensors:
            lost_energy = sensor.lost_energy(time_moving)
            sensor.remain_energy -= lost_energy
        self.cur_point = next_point
        return all_sensors
    def charging(self, time, all_sensors):
        for sensor in all_sensors:
            self.remain_MC_energy -= sensor.energy_receive(self.cur_point.x, self.cur_point.y)
            delta_e = sensor.energy_change_in_charging(time, self.cur_point.x, self.cur_point.y)
            sensor.update_energy(delta_e)
        return all_sensors
    def take_action(self, next_point, time, all_sensors):
        all_sensors = self.moving_to(next_point, all_sensors)
        all_sensors = self.charging(time, all_sensors)
        #print("\n-----------------\nThen:")
        #for sensor in all_sensors:
            #print("e = {:.4f}".format(sensor.get_remain_energy()))
        return all_sensors
    def check_energy(self):
        if(self.remain_MC_energy >= self.minumum_e):
            return 1
        return 0




class arguments():
  def __init__(self, hyper_lambda, hyper_beta):
    self.hyper_lambda = hyper_lambda
    self.hyper_beta = hyper_beta



    

if __name__ == '__main__':
    args = arg_parse() # get hyper-parameters
    all_sensors = []
    for i in range(10):
        x = random.random() * 8
        y = random.random() * 8
        energy_remain = random.random() * 30
        avg_consume_energy = random.random() * 2
        sensor = Sensor(x, y, energy_remain, avg_consume_energy)
        all_sensors.append(sensor)
    for sensor in all_sensors:
        print("\nEnergy remains: {:.4f} - avg_consume : {}".format(sensor.remain_energy, sensor.avg_consume_energy))
    D1 = Point(2,2)
    D2 = Point(-2, -1)
    D3 = Point(1, -2)
    MC = mobileCharger(args,1.5, Point(-3, -3))
    MC.take_action(D1, 0.15, all_sensors)
    MC.take_action(D2, 0.2, all_sensors)
    MC.take_action(D3, 0.26, all_sensors)

    
