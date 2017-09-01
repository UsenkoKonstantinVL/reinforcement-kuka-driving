from KUKA import robot
from obstacles import ObstacleContainer
from obstacles import get_regions, get_obstacles_in_regions
from neuralNetwork import *
from time import sleep
import random
import math
from copy import deepcopy


LOG_FILE_NAME = 'log\\log6.log'


def traing_network(network, robot, traing_rate=1000):

    network_q = deepcopy(network)
    #initialize goal point

    container = ObstacleContainer()
    container.update(robot.getCoordinate(), robot.unpack())
    goal_pos = get_goal_point(container)
    game = 1
    training_data = []

    train_eps = 0.4
    min_eps = 0.3
    eps = train_eps
    alpha = 0.9
    sigma = 0.8
    print("New goal: " + str(goal_pos))
    var_max_q = -100
    var_min_q = 100

    network.get_param(alpha, sigma)

    act_rand = 0
    act_net = 0

    average_act = 0

    ran = random.random()

    # TODO придумать условие завершения обучения
    while(game < 1000001):
        # 1 игра - 1 цикл
        # 1 эпизод - 100 игр или если робот достиг цели или врезался в препятствие
        # select action

        network_res = []
        container = ObstacleContainer()
        container.update(robot.getCoordinate(), robot.unpack(), robot.get_orientation())
        a1 = 0
        a2 = 0
        a3 = 0

        inpt, lidar_d = get_input_vec(container, goal_pos)

        # Управление роботом НС
        if ran < (1 - eps):
            a1, a2, a3, network_res = get_action(network, inpt)
            # a1, a2, a3, network_res = get_pid_action(robot, network, inpt)
            set_action(a1, a2, a3, robot)
            act_net += 1
        # else:
        #     # a1, a2, a3, network_res = get_action(network, inpt)
        #     a1, a2, a3, network_res = get_pid_action(robot, network, inpt)
        #     set_action(a1, a2, a3, robot)
        #     act_net += 1

        # Рандомное управление
        else:
            a1, a2, a3, network_res = get_random_actions(network, inpt)
            set_action(a1, a2, a3, robot)
            act_rand += 1

        eps = eps - (train_eps - min_eps) / 20000
        container.update(robot.getCoordinate(), robot.unpack(), robot.get_orientation())

        # get reward and maxQ
        m_q1, m_q2, m_q3, new_state = get_max_Q(network_q, container, goal_pos)
        reward = get_reward_with_collicion(robot, inpt[18], inpt[19], game)
        # НЕНУЖНЫЙ КОД
        # reward = get_reward_d(container, inpt[18], inpt[19], lidar_d, game)
        # compute current Q
        # network_res[a1] = network_res[a1] + alpha * (reward[0] + sigma * m_q1 - network_res[a1])
        # network_res[a2 + 3] = network_res[a2 + 3] + alpha * (reward[1] + sigma * m_q2 - network_res[a2 + 3])
        # network_res[a3 + 6] = network_res[a3 + 6] + alpha * (reward[2] + sigma * m_q3 - network_res[a3 + 6])
        # КОНЕЦ НЕНУЖНОГО КОДА

        # тренировочная дата: [входные данные, выходные данные]
        # training_data.append([inpt, network_res])
        # network.training(training_data)

        average_act += reward[0]
        average_act += reward[1]
        average_act += reward[2]

        # Формирование тренировочного массива
        train_data = [new_state, [a1, a2, a3], reward]# Новый тип данных
        training_data.append([inpt, train_data])
        # TODO Реализовать составление формирование данных для тренировки НС
        # TODO При столкновении перезапустить сцену
        raise NotImplemented()

        if (game % traing_rate) == 0:
            # тренировка
            # game = 0
            print("Training network")
            # При тренировки НС остановить робота
            robot.setVelocityVect(0, 0, 0)
            #network.training(training_data, N=10)
            # Тренировка НС
            network.training_newformatdata(training_data, N=10)
            network.save_nn()
            #training_data = []

        # Обновление копии НС, используемой для вычисления Q'
        if game % 1000 == 0:
            network_q = deepcopy(network)
            network.update_secondnn()

        # Обновление тренировочных данных
        if (game % (traing_rate * 10) == 0):
            training_data = []

        t_avegage_act = average_act

        # Вывод информации каждые 10 игр
        if game % 10 == 0:
            print("Game: " + str(game))
            print("Game data: " + str(container.pos) + " : " + str(container.orientation))
            print("Game data: " + str(inpt[18]) + " : " + str(inpt[19]))
            print("Game average reward: " + str(average_act / (3 * 10)))
            print("Goal: " + str(goal_pos))

            average_act = 0
            ran = random.random()

        # Конец эпизода
        collision = robot.check_collision()
        if (game % 100) == 0 or (inpt[18] < 0.125 or collision == 1):
            goal_pos = get_goal_point(container)
            print("Game probability: " + str(act_net) + ' :(rand) ' + str(act_rand))
            print("New goal: " + str(goal_pos))

            # При столкновении с препятствием перезапуск сцены
            if collision == 1:
                raise NotImplemented()
                robot.setVelocityVect(0, 0, 0)
                robot.restartscene()

            act_rand = 0
            act_net = 0
            save_log(LOG_FILE_NAME, game, var_max_q, var_min_q, t_avegage_act)
            t_avegage_act = 0

        game += 1
        # Конец цикла - игры

    network.save_nn()


def get_reward_d(container, distance, dphi, lidar_data, game):
    # ret_list = get_reward(container, distance, dphi, lidar_data)
    ret_list = get_reward_2(container, distance, dphi)
    coef = (-game % 100) / 2.0
    ret_list[0] += coef
    ret_list[1] += coef
    ret_list[2] += coef
    return ret_list


def get_reward_with_collicion(robot, distance, dphi, game):
    ret_list = [0, 0, 0]

    if robot.check_collision() == 1:
        ret_list = [-50, -50, -50]

    # if math.fabs(dphi) > 1:
    #     ret_list[1] += -10
    # elif math.fabs(dphi) > 0.5:
    #     ret_list[1] += -5
    # elif math.fabs(dphi) > 0.25:
    #     ret_list[1] += 2
    # elif math.fabs(dphi) > 0.1:
    #     ret_list[1] += 3
    # else:
    #     ret_list[1] += 10
    #
    if distance > 0.75:
        ret_list[0] += -10
    elif distance > 0.5:
        ret_list[0] += -2
    elif distance > 0.25:
        ret_list[0] += -1
    elif distance > 0.125:
        ret_list[0] += 2
    else:
        ret_list[2] = 50
        ret_list[1] = 50
        ret_list[0] = 50

    # if distance < 0.125:
    #     ret_list[2] = 50
    #     ret_list[1] = 50
    #     ret_list[0] = 50

    coef = (-game % 100) / 2.0
    ret_list[0] += coef
    ret_list[1] += coef
    ret_list[2] += coef
    return ret_list


def get_reward(container, distance, dphi, lidar_data):

    ret_list = [0, 0, 0]

    if distance > 0.75:
        ret_list[0] = -30
    elif distance > 0.5:
        ret_list[0] = -5
    elif distance > 0.25:
        ret_list[0] = -1
    elif distance > 0.125:
        ret_list[0] = 5
    else:
        ret_list[0] = 30

    if lidar_data[7] > 1 or lidar_data[8] > 1 or lidar_data[9] > 1 or lidar_data[10] > 1:
        ret_list[0] += 30# min(lidar_data[7], lidar_data[8], lidar_data[9], lidar_data[10])
        ret_list[1] += 10
    elif lidar_data[7] > 0.4 or lidar_data[8] > 0.4 or lidar_data[9] > 0.4 or lidar_data[10] > 0.4:
        ret_list[0] += -2
        ret_list[1] += -5
        ret_list[2] += -5
    else:
        ret_list[0] += -20
        ret_list[1] += -20
        ret_list[2] += -25

    if math.fabs(dphi) > 1:
        ret_list[1] += -10
    elif math.fabs(dphi) > 0.5:
        ret_list[1] += -2
    elif math.fabs(dphi) > 0.25:
        ret_list[1] += 2
    elif math.fabs(dphi) > 0.1:
        ret_list[1] += 5
    else:
        ret_list[1] += 10

    if (lidar_data[0] or lidar_data[1] or lidar_data[2] or lidar_data[3] or lidar_data[4] or lidar_data[5] or lidar_data[6]) > 1:
        ret_list[2] += 10
    elif (lidar_data[0] or lidar_data[1] or lidar_data[2] or lidar_data[3] or lidar_data[4] or lidar_data[5] or lidar_data[6]) > 0.4:
        ret_list[2] += 0
    else:
        ret_list[2] += -50

    if (lidar_data[11] or lidar_data[12] or lidar_data[13] or lidar_data[14] or lidar_data[15] or lidar_data[16] or lidar_data[17]) > 1:
        ret_list[2] += 10
    elif (lidar_data[11] or lidar_data[12] or lidar_data[13] or lidar_data[14] or lidar_data[15] or lidar_data[16] or lidar_data[17]) > 0.4:
        ret_list[2] += 0
    else:
        ret_list[2] += -50

    if distance < 0.07:
        ret_list[0] = 100
        ret_list[1] = 100
        ret_list[2] = 100

    return ret_list
    # TODO реализовать получение вознаграждения
    # raise Exception("Implement get_reward method in main.py")
    # return [0, 0, 0]


def get_reward_2(container, distance, dphi):
    list_regions = get_obstacles_in_regions(container.obs)

    ret_list = [0, 0, 0]

    if distance > 0.75:
        ret_list[0] = -30
    elif distance > 0.5:
        ret_list[0] = -5
    elif distance > 0.25:
        ret_list[0] = -1
    elif distance > 0.125:
        ret_list[0] = 5
    else:
        ret_list[0] = 30

    if math.fabs(dphi) > 1:
        ret_list[1] += -10
    elif math.fabs(dphi) > 0.5:
        ret_list[1] += -2
    elif math.fabs(dphi) > 0.25:
        ret_list[1] += 2
    elif math.fabs(dphi) > 0.1:
        ret_list[1] += 5
    else:
        ret_list[1] += 50

    if list_regions[2] > 1:
        ret_list[1] += 10
        ret_list[0] += 10
    elif list_regions[2] > 0.5:
        ret_list[1] += 0
        ret_list[0] += 0
    elif list_regions[2] > 0.2:
        ret_list[1] += -10
        ret_list[0] += -10
    else:
        ret_list[1] += -20
        ret_list[0] += -20

    if list_regions[1] < 0.2 or list_regions[4] < 0.2:
        ret_list[2] += -20
    elif list_regions[1] < 0.5 or list_regions[4] < 0.5:
        ret_list[2] += -5
    else:
        ret_list[2] += 10

    if distance < 0.07:
        ret_list[0] = 100
        ret_list[1] = 100
        ret_list[2] = 100

    return ret_list


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
    #print(res)

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

    return act1, act2, act3, inpt


def set_action(act1, act2, act3, robot):
    vel = 0
    steer = 0
    s_vel = 0

    # steer: 1-right, 2-left

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


def get_pid_action(robot, network, inpt):
    distance = inpt[18]
    dphi = inpt[19]

    action1 = 0
    action2 = 0
    action3 = 0

    if dphi > 0.1:
        action2 = 2
    elif dphi < -0.1:
        action2 = 1

    if distance < 0.075:
        action1 = 0
        action2 = 0
        action3 = 0
    else:
        action1 = 1

    if math.fabs(dphi) > 0.8:
        action1 = 0

    if robot.check_collision() == 1:
        action1 = 2
        action2 = 0
        action3 = 0

    res = network.get_prediction(inpt)
    return action1, action2, action3, res


def get_random_actions(network, inpt):
    action1 = random.randint(0, 2)
    action2 = random.randint(0, 2)
    action3 = random.randint(0, 2)
    res = network.get_prediction(inpt)
    return action1, action2, action3, res


def get_input_vec(container, goal_pos):
    inpt = []

    lidar_data = get_regions(container)

    len = distance_between(container.pos, goal_pos)
    dphi = get_dphi(container.pos, goal_pos)

    dphi = dphi - container.orientation

    if dphi > math.pi:
        dphi = -2*math.pi + dphi
    elif dphi < -math.pi:
        dphi = 2 * math.pi + dphi

    inpt.extend(lidar_data)
    inpt.append(len)
    inpt.append(dphi)
    return inpt, lidar_data


def get_action(network, inpt):
    res = network.get_prediction(inpt)

    act1 = 0
    act2 = 0
    act3 = 0

    max_q = res[0]
    l = 0
    for i in range(3):
        n = i + l
        if res[n] > max_q:
            max_q = res[n]
            act1 = i

    max_q = res[3]
    l = 3
    for i in range(3):
        n = i + l
        if res[n] > max_q:
            max_q = res[n]
            act2 = i

    max_q = res[6]
    l = 6
    for i in range(3):
        n = i + l
        if res[n] > max_q:
            max_q = res[n]
            act3 = i

    return act1, act2, act3, res


def distance_between(pos1, pos2):
    len = math.sqrt(
        math.pow(pos1[0] - pos2[0], 2) +
        math.pow(pos1[1] - pos2[1], 2)
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
    # print("Old coordinate: " + str(pos))
    dlen = random.uniform(1, 3)
    dphi = random.uniform(-1, 1)

    x = pos[0] + dlen * math.cos(dphi * math.pi)
    y = pos[1] + dlen * math.sin(dphi * math.pi)

    goal_pos = [x, y]

    if goal_pos[0] < -4.9:
        goal_pos[0] = -4.5
    elif goal_pos[0] > 5:
        goal_pos[0] = 4.5

    if goal_pos[1] > 8.5:
        goal_pos[1] = 7.5
    elif goal_pos[1] < -3:
        goal_pos[1] = -2.5

    return goal_pos

def save_log(log_name, i, max_q, min_q, aver_rew):
    with open(log_name, 'a') as out:
        out.write(str(i) + ',' + str(max_q) + ',' + str(min_q) + ',' + str(aver_rew) + '\n')

if __name__ == '__main__':

    robot = robot()
    robot.start_simulation()
    robot.initialize()
    robot.getCoordinate()
    robot.check_collision()
    network = LearningNetwork_3("ten")
    # network.open_nn()

    traing_network(network, robot, traing_rate=500)

    robot.finish_simulation()
