import numpy as np
import time

class Sensor:
    """ This class is built to work with sensors in the network."""

    def __init__(self, x, y, remain_energy, avg_consume_energy):

        self.x_axis = x
        self.y_axis = y
        self.remain_energy = remain_energy
        self.avg_consume_energy = avg_consume_energy
        self.hyper_lambda = 0.45    #constant
        self.hyper_beta = 0.8       #constant

    def get_remain_energy(self):
        return self.remain_energy

    def lost_energy(self, time):
        remains = self.get_remain_energy() - time * self.avg_consume_energy
        return remains

    def energy_receive(self, x_D, y_D):
        received = (
            self.hyper_lambda
            / (
                np.sqrt((self.x_axis - x_D) ** 2 + (self.y_axis - y_D) ** 2)
                + self.hyper_beta
            )
            ** 2
        )
        return received

    def energy_change_in_charging(self, time, x_D, y_D):
        change = (
            self.energy_receive(x_D, y_D)
            - self.avg_consume_energy
        ) * time
        return change

    def update_energy(self, delta_energy):
        self.remain_energy = self.remain_energy + delta_energy

    def check_energy(self, E_min, requests):
        if self.get_remain_energy() < E_min:
            requests = self.send_request(requests)
        return requests

    def send_request(self, requests):
        seconds_now = int(round(time.time()))
        rq = Request(seconds_now, self)
        requests.append(rq)
        return requests

    def mc_moving(self, x_D, y_D):
        print("Initial energy of sensor 1 is: {}\n".format(self.remain_energy))
        print("After: \n")
        change = self.energy_change_in_time(0.5, x_D, y_D)
        self.update_energy(change)
        print("Final energy of sensor 1 is: {}\n".format(self.remain_energy))

class Request():
  def __init__(self, time_sent, sensor):
    self.time_sent = time_sent
    self.sensor_rq = sensor
