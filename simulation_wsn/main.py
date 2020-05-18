from environment import *
import matplotlib.pyplot as plt
import time
import numpy as np
import random
import threading

def randomData():
    # random a lists of sensors
    Points = (np.random.uniform(-5, 5, (20,2)))
    E0 = abs(np.random.uniform(0,40, (20,1)))
    avg_comsume_e = abs(np.random.randn(20,1))
    Sensors_vector = np.hstack((Points, E0, avg_comsume_e))
    num_sensor = Sensors_vector.shape[0]
    all_sensors = []
    for i in range (num_sensor):
        sensor = Sensor(Sensors_vector[i,0], Sensors_vector[i,1], Sensors_vector[i,2], Sensors_vector[i,3])
        all_sensors.append(sensor)
    #for sensor in all_sensors:
        #print("\nEnergy remains: {:.4f} - avg_consume : {:.4f}".format(sensor.get_remain_energy(), sensor.avg_consume_energy))

# Make array of charger points
    grid = make_grid(Sensors_vector)
    charging_points = grid
    return all_sensors, charging_points, Points

def make_grid(sensors_copy):
  grids = []
  for i in np.linspace(min(sensors_copy[:,0])+0.5, max(sensors_copy[:,0])-0.5, 5):
    for j in np.linspace(min(sensors_copy[:,1])+0.5, max(sensors_copy[:,1])-0.5, 5):
      grids.append([i,j])
  return grids

def plot(grid, Points):
    # plot charger points.
    time.sleep(2)

    x_val = [x[0] for x in grid]
    y_val = [x[1] for x in grid]


    plt.plot(x_val,y_val,'or')
    plt.plot(Points[:,0], Points[:,1], 'bx')
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()



# Main process
class runFirst(threading.Thread):
    def run(self):
        all_sensors, charging_points, Points = randomData()
        args = arguments(80, 0.4)
        requests = []
        requests_2 = []
        MC = mobileCharger(args, 5, Point(-3, -3))
        env = Environment(requests,charging_points)



def processMain(all_sensors, MC, env):
    env.update_requests(all_sensors)
    all_sensors, MC = env.process_requests(all_sensors, MC)
    return all_sensors, MC
    

def update_RQ(all_sensors, requests_2):
    for sensor in all_sensors:
        request2 = sensor.check_energy(5, requests_2)
    return request2


class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self, all_sensors, MC, env):
      print ("Starting " + self.name)
      all_sensors, MC = processMain(all_sensors, MC, env)
      print ("Exiting " + self.name)

class myThread2 (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self, all_sensors, requests_2):
      print ("Starting " + self.name)
      requests_2 = update_RQ(all_sensors, requests_2)
      print ("Exiting " + self.name)


"""
# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread2(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()
"""
t = time.time()

all_sensors, charging_points, Points = randomData()
args = arguments(80, 0.4)
requests = []
requests_2 = []
MC = mobileCharger(args, 5, Point(-3, -3))
env = Environment(requests,charging_points)

thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread2(2, "Thread-2", 2)

# Start new Threads
thread1.run(all_sensors, MC, env)
thread2.run(all_sensors, requests_2)
print(requests_2[0].time_sent)

for i in range(len(requests_2)):
    print(requests_2[i].time_sent)
print ("done in ", time.time()- t)

"""

t1 = threading.Thread(target=processMain, args=(all_sensors, MC, env,))
t2 = threading.Thread(target=update_RQ, args=(all_sensors, requests_2, ))
t1.start()
t2.start()
t1.join()
t2.join()
print(requests_2[0].time_sent)
print(len(requests_2))
print ("done in ", time.time()- t)
"""
