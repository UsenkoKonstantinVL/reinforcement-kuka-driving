from KUKA import robot
from obstacles import ObstacleContainer
from obstacles import get_regions
from neuralNetwork import LearningNetwork
from time import sleep
import random
import math


def traing_network(network, robot, traing_rate = 1000):
    #initialize goal point
    container = ObstacleContainer()
    container.update(robot.getCoordinate(), robot.unpack())
    goal_pos = get_goal_point(container)
    game = 1
    training_data = []

#TODO придумать условие завершения обучения
    while(True):
        # select action
        eps = 0.8
        alpha = 0.9
        sigma = 0.1

        network_res = []
        container = ObstacleContainer()
        container.update(robot.getCoordinate(), robot.unpack())
        a1 = 0
        a2 = 0
        a3 = 0

        inpt = get_input_vec(robot, goal_pos)
        if random.random() < eps:
            a1, a2, a3, network_res = get_action(network, inpt)
            set_action(a1, a2, a3)
        else:
            a1, a2, a3, network_res = get_random_actions()
            set_action(a1, a2, a3)

        #get reward and maxQ
        m_q1, m_q2, m_q3 = get_max_Q(network, robot, goal_pos)
        reward = get_reward()
        #compute current Q
        network[a1] = network[a1] + alpha * (reward[0] + sigma * m_q1 - network[a1])
        network[a2 + 3] = network[a2 + 3] + alpha * (reward[1] + sigma * m_q2 - network[a2 + 3])
        network[a3 + 6] = network[a3 + 6] + alpha * (reward[2] + sigma * m_q3 - network[a3 + 6])

        # тренировочная дата: [входные данные, выходные данные]
        training_data.append([inpt, network])


        if (game % traing_rate) == 1:
            # тренировка
            game = 0
            robot.setVelocityVect(0, 0, 0)
            network.training(training_data)
            network.save_nn()
            training_data = []

        if (game % 100) == 1 or (inpt[18] < 0.05):
            goal_pos = get_goal_point(container)

        game += 1

def get_reward():
    #TODO реализовать получение вознаграждения
    return [0, 0, 0]

def get_max_Q(network, container, goal_pos):
    # container = ObstacleContainer()
    # container.update(robot.getCoordinate(), robot.unpack())
    inpt = []

    lidar_data = get_regions(container)

    len = distance_between(container.pos, goal_pos)
    dphi = get_dphi(container.pos, goal_pos)

    inpt.extend(lidar_data)
    inpt.append(len)
    inpt.append(dphi)

    res = network.get_prediction(inpt)

    act1 = 0
    act2 = 0
    act3 = 0

    max_q = 0
    l = 0
    for i in range(3):
        n = i + l
        if res[n] > max_q:
            max_q = res[n]
            act1 = max_q

    max_q = 0
    l += 3
    for i in range(3):
        n = i + l
        if res[n] > max_q:
            max_q = res[n]
            act2 = max_q

    max_q = 0
    l += 3
    for i in range(3):
        n = i + l
        if res[n] > max_q:
            max_q = res[n]
            act3 = max_q

    return act1, act2, act3

def set_action(act1, act2, act3, robot):
    vel = 0
    steer = 0
    s_vel = 0

    if act1 == 1:
        vel = 1
    elif act1 == 2:
        vel = -1

    if act2 == 1:
        steer = 1
    elif act2 == 2:
        steer = -1

    if act3 == 1:
        s_vel = 1
    elif act3 == 2:
        s_vel = -1

    robot.setVelocityVect(vel, steer, s_vel)

def get_random_actions():
    action1 = random.randint(0, 3)
    action2 = random.randint(0, 3)
    action3 = random.randint(0, 3)
    return action1, action2, action3

def get_input_vec(container, goal_pos):
    inpt = []

    lidar_data = get_regions(container)

    len = distance_between(container.pos, goal_pos)
    dphi = get_dphi(container.pos, goal_pos)

    inpt.extend(lidar_data)
    inpt.append(len)
    inpt.append(dphi)
    return inpt

def get_action(network, inpt):
    # container = ObstacleContainer()
    # container.update(robot.getCoordinate(), robot.unpack())
    # inpt = []
    #
    # lidar_data = get_regions(container)
    #
    # len = distance_between(container.pos, goal_pos)
    # dphi = get_dphi(container.pos, goal_pos)
    #
    # inpt.extend(lidar_data)
    # inpt.append(len)
    # inpt.append(dphi)

    res = network.get_prediction(inpt)

    act1 = 0
    act2 = 3
    act3 = 6

    max_q = 0
    l = 0
    for i in range(3):
        n = i + l
        if res[n] > max_q:
            max_q = res[n]
            act1 = i

    max_q = 0
    l += 3
    for i in range(3):
        n = i + l
        if res[n] > max_q:
            max_q = res[n]
            act2 = i

    max_q = 0
    l += 3
    for i in range(3):
        n = i + l
        if res[n] > max_q:
            max_q = res[n]
            act3 = i


    return act1, act2, act3, res

def distance_between(pos1, pos2):
    len =  math.sqrt(
        math.pow(pos1[0] + pos2[0], 2) +
        math.pow(pos1[1] + pos2[1], 2)
    )

    if len > 4.0:
        len = 4.0
    return float(len)/4.0

def get_dphi(pos1, pos2):
    dphi = math.atan2(pos2[1] - pos1[1],
                      pos2[0] - pos1[0])

    dphi = dphi / math.pi
    return  dphi

def get_goal_point(container):
    pos = container.pos
    r = random()
    dlen = random.uniform(2, 4)
    dphi = random.uniform(-1, 1)

    x = pos[0] + dlen * math.cos(dphi * math.pi)
    y = pos[1] + dlen * math.sin(dphi * math.pi)

    goal_pos = [x, y]

    # dx = 2 + random.uniform(0, 2)
    # dy = 2 + random.uniform(0, 2)
    # goal_pos = [pos[0] + dx , pos[1] + dy]

    return goal_pos



if __name__ == '__main__':
    # robot = robot()
    # robot.start_simulation()
    # robot.initialize()
    # r = robot.getLaserPoints()
    # print(robot.unpack(r))
    # robot.finish_simulation()
    print(get_random_actions())
    robot = robot()
    robot.start_simulation()
    robot.initialize()
    print(robot.getCoordinate())
    print(robot.getCoordinate())
    print(robot.getLaserPoints())
    # network = LearningNetwork("Example")
    # inpt = get_input_vec(robot, [0.5, 0.2])
    # print(get_action(network, inpt))

    sleep(0.1)
    robot.setVelocityVect(0.5, 0, 0)
    sleep(2)
    robot.setVelocityVect(0, 0.5, 0)
    sleep(2)
    robot.setVelocityVect(0, 0, 0.5)
    sleep(2)
    robot.setVelocityVect(0, 0, 0)

    robot.finish_simulation()