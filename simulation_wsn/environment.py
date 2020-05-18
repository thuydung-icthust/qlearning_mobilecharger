import numpy as np
from mobile_charger import *
from sensor import *

class Environment:
    def __init__(self, requests, charging_points):
        self.requests = requests
        self.charging_points = charging_points

    def update_requests(self, all_sensors):
        for sensor in all_sensors:
            self.requests = sensor.check_energy(5, self.requests)

    # no longer in use. 
    
    def dequeue_request(self):
        target_sensor = self.requests[0].sensor_rq
        next_point = self.findgrid(self.charging_points, target_sensor)
        self.requests.remove(self.requests[0])
        return next_point


    def process_requests(self, all_sensors, MC):
        while (len(self.requests) >= 0) and (MC.check_energy() == 1):
            next_point = self.dequeue_request()
            charge_time = random.random()
            all_sensors = MC.take_action(next_point, charge_time, all_sensors)
            print("\n-----------------\nThen:")
            for sensor in all_sensors:
                print("e = {:.4f}".format(sensor.remain_energy))
        return all_sensors, MC

    """
    def findgrid(self, grids, s):
        # find the grid that is closest to the requested sensor
        dis = []
        sensor_pos = Point(s.x_axis, s.y_axis)
        # print(sensor_pos.x, sensor_pos.y)

        for grid in grids:
            charging_point = Point(grid[0], grid[1])
            d = np.sqrt(
                (sensor_pos.x - charging_point.x) ** 2
                + (sensor_pos.y - charging_point.y) ** 2
            )
            dis.append(d)
        dis = np.array(dis)
        # print(grids[np.argmin(dis)])
        result = grids[np.argmin(dis)]
        return Point(result[0], result[1])
    """


