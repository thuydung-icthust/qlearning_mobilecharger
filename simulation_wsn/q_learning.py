import pulp as p
import numpy as np 
import time

def update_energy_value(requests, next_pos, para_lambda, para_beta):
  time_now = int(time.time() * 1000)
  E1 = []
  ej = []
  pj = []
  for rq in requests:
  #print(rq.energy_remain)
    e1 = rq.sensor_rq.remain_energy - rq.sensor_rq.avg_consume_energy * (time_now - rq.time_sent)
    E1.append(e1)
    ej.append(rq.sensor_rq.avg_consume_energy)
    pj.append(rq.sensor_rq.energy_receive(next_pos[0], next_pos[1], para_lambda, para_beta))
  E1 = np.asarray(E1)
  ej = np.asarray(ej)
  pj = np.asarray(pj)
  E1.reshape(len(requests), 1)
  ej.reshape(len(requests), 1)
  pj.reshape(len(requests), 1)
  return E1, ej, pj

#E1, ej, pj = update_energy_value(requests, next_pos, MC.hyper_lambda, MC.hyper_beta)

#len(charging_points)
#alpha = 0.65

def find_Ti(num_sensors, time_moving, avg_consume_MC, E_move, E_star, E1, ej, pj):

  M = 999999999
  set_a = range(0, num_sensors)
  Lp_prob = p.LpProblem("Find time Ti", p.LpMaximize)
  Ti = p.LpVariable("Ti", lowBound=0)
  a = p.LpVariable.dicts("a", set_a, cat='Continuous')

  for i in range(num_sensors):
    Lp_prob += a[i] >= 0
    Lp_prob += a[i] <= 1
    Lp_prob += (E1[i] - time_moving* ej[i] + (pj[i] - ej[i]) * Ti) >= E_star - M*(1-a[i])
    Lp_prob += (E1[i] - time_moving* ej[i] + (pj[i] - ej[i]) * Ti) <= E_star + M*a[i]
  #  Lp_prob += (5 - time_moving* 10 + (0.8 * Ti)) >= E_star - M*(1-a[i])
  #  Lp_prob += (5 - time_moving* 10 + (0.8 * Ti)) <= E_star + M*(a[i])
  Lp_prob += E_move + sum(sum(pj * Ti)) <= MC.remain_MC_energy
  Lp_prob += p.lpSum([a[i] for i in set_a])
  #print(Lp_prob) 
  #p.LpSolverDefault.msg = 1
  status = Lp_prob.solve()   # Solver 
  Lp_prob.solve()
  #print(p.LpStatus[status])   # The solution status 
  #print(p.value(Ti))

  N0 = int(sum(np.array([a[i].varValue for i in set_a])))
  return p.value(Ti), N0

def reward(requests, E2, ej, pj, N0):
  reward = 0
  for i in range(0, len(requests)):
    reward = reward + 1.0/E2[i] * (pj[i]/ej[i]- 1)

  reward = reward + N0/len(requests)
  return reward

def update_energy_part2(requests, next_pos, para_lambda, para_beta):
  #time_now = int(time.time() * 1000)
  pj = []
  for rq in requests:
  #print(rq.energy_remain)
    pj.append(rq.sensor_rq.energy_receive(next_pos[0], next_pos[1], para_lambda, para_beta))
  pj = np.asarray(pj)
  pj.reshape(len(requests), 1)
  return pj

def find_Q_max(requests, charging_points, cur_pos, mc_velocity, avg_consume_MC, E_move, E_star, E2, ej):
  #index = 0
  max_reward = 0
  for i in range(len(charging_points)):
    nextpos = charging_points[i]
    #if(nextpos == cur_pos):
      #continue
    time_moving = np.sqrt((cur_pos[0] - nextpos[0])**2 + (cur_pos[1] - nextpos[1]) ** 2) / mc_velocity
    pj = update_energy_part2(requests, nextpos, MC.hyper_lambda, MC.hyper_beta)
    Ti_2, N0_2 = find_Ti(len(requests), time_moving, avg_consume_MC, E_move, E_star, E2, ej, pj)
    E3 = E2 - time_moving* ej+ (pj- ej) * Ti_2
    rw = reward(requests, E3, ej, pj, N0_2)
    if(max_reward < rw):
      max_reward = rw
      #index = i
  
  return max_reward

def update_Qvalue(requests, Q_table, T_table, charging_points, cur_pos, mc_velocity , avg_consume_MC, E_move, E_star, hyp_alpha):
  num_sensors = len(requests)
# E1, ej, pj = update_energy_value(requests, )

  for i in range(len(charging_points)):
    next_pos = charging_points[i]
    rw = 0
    E1, ej, pj = update_energy_value(requests, next_pos, MC.hyper_lambda, MC.hyper_beta )
    time_moving = np.sqrt((cur_pos[0] - next_pos[0])**2 + (cur_pos[1] - next_pos[1]) ** 2) / mc_velocity
    Ti, N0 = find_Ti(num_sensors, time_moving, avg_consume_MC, E_move, E_star, E1, ej, pj)
    T_table[i] = Ti
    E2 = E1 - time_moving* ej+ (pj- ej) * Ti
    rw = reward(requests,E2, ej, pj, N0)
    Q_max = find_Q_max(requests, charging_points, cur_pos, mc_velocity, avg_consume_MC, E_move, E_star, E2, ej)
    # Update Q-value
    Q_table[i] = (1-hyp_alpha) * Q_table[i] + hyp_alpha * (rw + Q_max)
  return Q_table, T_table, E2

def update_requests(requests, next_point, time_charging, E_star, E2):
  for i in range(len(requests)):
    if(E2[i] >= E_star):
      requests.remove[i-1:i]
  return requests

def take_action(Q_table, T_table, charging_points):
  index = np.argmax(Q_table)
  next_point = charging_points[index]
  time_charging = T_table[index]