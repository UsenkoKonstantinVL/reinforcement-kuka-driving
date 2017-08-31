import math


class ObstacleContainer:
    def __init__(self, pos=[], orient=0):
        self.obs = []
        self.pos = pos
        self.orientation = orient
    # obs - массив точек координат [x, y]

    # Добавление и фильтрация новых данных с ЛИДАРа
    def update(self, pos, points, dphi=0):
        new_pos = []
        self.pos = pos
        self.orientation = dphi

        self.update_obstacles()

        self.obs = []

        for p in points:
            if p[0] == p[1] == 0: continue
            new_x = ((int)(p[0] * 1000))/1000.0
            new_y = ((int)(p[1] * 1000))/1000.0
            # new_pos.append([new_x, new_y])
            self.obs.append([new_x, new_y])


        # for p in new_pos:
        #     if not self.is_сontain(p):
        #         self.obs.append(p)
        # self.update_obstacles()

    # Фильтрация точек: Если точка в массиве obs не входит в прямоугольную обасть вокруг робота
    def update_obstacles(self):
        new_obs = []
        for p in self.obs:
            if (abs(p[0] - self.pos[0]) <= 2.5) and (abs(p[1] - self.pos[1]) <= 2.5):
                new_obs.append(p)
        self.obs = new_obs
        '''
        new_obs = []
        for obs in self.obs:
            if not self.get_distance(obs, self.pos) > 2.5:
                new_obs.append(obs)
        self.obs = new_obs
        '''

    def get_obs(self):
        return self.obs

    # Возвращает приведенные к центру робота координаты точек
    def get_norm_obs(self):
        new_obs = []

        for p in self.obs:
            new_x = p[0] - self.pos[0]
            new_y = p[1] - self.pos[1]

            new_obs.append([new_x, new_y])

        return new_obs

    # Если такая точка имеется, то возвращаем True
    def is_сontain(self, obs_pos):
        for obs in self.obs:
            if obs_pos[0] == obs[0] and obs_pos[1] == obs[1]:
                return True
        return False

    @staticmethod
    def get_distance(obs_pos, pos):
        return math.sqrt(math.pow(pos[0] - obs_pos[0], 2) + math.pow(pos[1] - obs_pos[1], 2))


# Возвращает ближайшую точку в регионе
def get_regions(obstacle):
    # _res = obstacle.get_norm_obs()
    _res = list(obstacle.get_obs())
    res = []

    # for i in _res:
    #     res.append(i)

    N = 18
    reg = []

    da = (180 / N) * math.pi / 180

    for i in range(N):
        reg.append(10)

    alpha = math.pi/2 - da

    for point in _res:
        if (math.atan2(point[1], point[0]) >= -math.pi/2) and (math.atan2(point[1], point[0]) <= math.pi/2):
            res.append(point)

    for i in range(N):
        n_alpha = alpha - da * i
        mass_j = []

        for j, val in enumerate(res):
            if(math.atan2(val[1], val[0]) >= n_alpha):
                mass_j.append(j)

        min_len = reg[i]
        for k in mass_j:
            dist = get_distance(res[k])
            if(dist < min_len):
                min_len = dist

        reg[i] = min_len

        list_to_delete = []

        for k in mass_j:
            list_to_delete.append(res[k])

        for k in list_to_delete:
            res.remove(k)

    return reg


def get_obstacles_in_regions(obstacles):
    list_regions = [10, 10, 10, 10, 10]

    for obstacle in obstacles:
        if obstacle[0] < 0:
            if obstacle[1] > 0:
                if(list_regions[0] > obstacle[1]):
                    list_regions[0] = obstacle[1]
            else:
                if (list_regions[4] > -obstacle[1]):
                    list_regions[4] = -obstacle[1]
        else:
            if obstacle[1] > -0.2 and obstacle[1] < 0.2:
                if (list_regions[2] > obstacle[0]):
                    list_regions[2] = obstacle[0]
            elif obstacle[1] <= -0.2 and obstacle[0] < 0.5:
                if (list_regions[3] > -obstacle[1]):
                    list_regions[3] = -obstacle[1]
            elif obstacle[1] >= 0.2 and obstacle[0] < 0.5:
                if (list_regions[1] > obstacle[1]):
                    list_regions[1] = obstacle[1]

    return list_regions


def get_distance(landmark):
    return math.sqrt(math.pow(landmark[0], 2) + math.pow(landmark[1], 2))
