from neupy import layers, algorithms, init
import dill
import numpy as np
from copy import deepcopy

class LearningNetwork:
    def __init__(self, network_name):
        self.network_name = network_name
        self.file = 'network\\' + self.network_name + '.net'
        self.initialize()

    # Инициализация нейронной сети
    def initialize(self):
        self.network = algorithms.Momentum(
            [
                layers.Input(20),
                layers.Relu(30, weight=init.Uniform(-1, 1)),
                layers.Tanh(40, weight=init.Uniform(-1, 1)),
                # layers.Embedding(40, 1),
                # layers.GRU(40),
                layers.Relu(25, weight=init.Uniform(-1, 1)),
                layers.Linear(9, weight=init.Uniform(-1, 1)),
            ],

            error='categorical_crossentropy',
            step=0.01,
            verbose=False,
            shuffle_data=True,

            momentum=0.99,
            nesterov=True,

        )
        self.network.architecture()
        # self.network = algorithms.Momentum(
        #     [
        #         layers.Input(20),
        #         layers.GRU(40),
        #         layers.Relu(40),
        #         layers.Relu(25),
        #         layers.Linear(9),
        #     ],
        #
        #     error='categorical_crossentropy',
        #     step=0.01,
        #     verbose=True,
        #     shuffle_data=True,
        #
        #     momentum=0.99,
        #     nesterov=True,
        #
        # )

    # Вычисление Q значений
    def get_prediction(self, input):
        ret = self.network.predict(np.array(input))
        #print()
        return ret[0]

    # Тренировка НС
    def training(self, train_data, N=3):
        train_mtrx = []
        out_mtrx = []

        for var in train_data:
            train_mtrx.append(var[0])
            out_mtrx.append(var[1])
        self.network.train(np.array(train_mtrx), np.array(out_mtrx), epochs=N)#([np.array(var[0])], [np.array(var[1])], epochs=N)
        print(self.network.errors)

    # Сохранение НС
    def save_nn(self):
        with open(self.file, 'wb') as f:
            dill.dump(self.network, file=f)

    # Открытие НС
    def open_nn(self):
        with open(self.file, 'rb') as in_strm:
            self.network = dill.load(in_strm)
            #return n_network

class LearningNetwork_2:

    def __init__(self, network_name):
        self.network_name = network_name
        self.file = 'network\\' + self.network_name + '.net'
        self.initialize()

    # Инициализация нейронной сети
    def initialize(self):
        self.network = algorithms.Momentum(
            [
                layers.Input(20),
                # layers.LeakyRelu(20, weight=init.Uniform(-0.5, 0.5)) > layers.BatchNorm() > layers.Relu(),
                # layers.LeakyRelu(20, weight=init.Uniform(-0.5, 0.5)) > layers.BatchNorm() > layers.Relu(),
                # layers.Embedding(40, 1),
                # layers.GRU(40),
                layers.Linear(18, weight=init.Uniform(-0.5, 0.5)) ,
                layers.LeakyRelu(15, weight=init.Uniform(-0.5, 0.5)),
                layers.Linear(9, weight=init.Uniform(-0.5, 0.5)),
            ],

            error='categorical_crossentropy',
            step=0.01,
            verbose=False,
            shuffle_data=True,

            momentum=0.99,
            nesterov=True,

        )
        self.network.architecture()
        # self.network = algorithms.Momentum(
        #     [
        #         layers.Input(20),
        #         layers.GRU(40),
        #         layers.Relu(40),
        #         layers.Relu(25),
        #         layers.Linear(9),
        #     ],
        #
        #     error='categorical_crossentropy',
        #     step=0.01,
        #     verbose=True,
        #     shuffle_data=True,
        #
        #     momentum=0.99,
        #     nesterov=True,
        #
        # )

    # Вычисление Q значений
    def get_prediction(self, input):
        ret = self.network.predict(np.array(input))
        #print()
        return ret[0]

    # Тренировка НС
    def training(self, train_data, N=3):
        train_mtrx = []
        out_mtrx = []

        for var in train_data:
            train_mtrx.append(var[0])
            out_mtrx.append(var[1])
        self.network.train(np.array(train_mtrx), np.array(out_mtrx), epochs=N)#([np.array(var[0])], [np.array(var[1])], epochs=N)
        print(self.network.errors)

    # Сохранение НС
    def save_nn(self):
        with open(self.file, 'wb') as f:
            dill.dump(self.network, file=f)

    # Открытие НС
    def open_nn(self):
        with open(self.file, 'rb') as in_strm:
            self.network = dill.load(in_strm)
            #return n_network

class LearningNetwork_3:

    def __init__(self, network_name):
        self.network_name = network_name
        self.file = 'network\\' + self.network_name + '.net'
        self.alpha = 0
        self.sigma = 0
        self.initialize()


    def get_param(self, alpha, sigma):
        self.alpha = alpha
        self.sigma = sigma

    # Инициализация нейронной сети
    def initialize(self):
        self.network = algorithms.Momentum(
            [
                layers.Input(20),
                layers.Linear(20, weight=init.Uniform(-0.5, 0.5)) ,
                layers.LeakyRelu(15, weight=init.Uniform(-0.5, 0.5)),
                # layers.LeakyRelu(15, weight=init.Uniform(-0.5, 0.5)),
                # layers.LeakyRelu(12, weight=init.Uniform(-0.5, 0.5)),
                layers.Linear(9, weight=init.Uniform(-0.5, 0.5)),
            ],

            error='categorical_crossentropy',
            step=0.01,
            verbose=False,
            shuffle_data=True,

            momentum=0.99,
            nesterov=True,

        )
        self.network.architecture()

        self.update_secondnn()
        # self.network = algorithms.Momentum(
        #     [
        #         layers.Input(20),
        #         layers.GRU(40),
        #         layers.Relu(40),
        #         layers.Relu(25),
        #         layers.Linear(9),
        #     ],
        #
        #     error='categorical_crossentropy',
        #     step=0.01,
        #     verbose=True,
        #     shuffle_data=True,
        #
        #     momentum=0.99,
        #     nesterov=True,
        #
        # )

    # Вычисление Q значений
    def get_prediction(self, input):
        ret = self.network.predict(np.array(input))
        return ret[0]

    def get_predict_withcopynn(self, input):
        ret = self.network.predict(np.array(input))
        return ret[0]

    def update_secondnn(self):
        self.network_q = deepcopy(self.network)

    # Тренировка НС
    def training(self, train_data, N=3):
        train_mtrx = []
        out_mtrx = []

        for var in train_data:
            train_mtrx.append(var[0])
            out_mtrx.append(var[1])
        self.network.train(np.array(train_mtrx), np.array(out_mtrx), epochs=N)#([np.array(var[0])], [np.array(var[1])], epochs=N)
        print(self.network.errors)

    def training_newformatdata(self, train_data, N=3):
        # Формат входных данных: [s, s', r, a] - {текущее состояние, новое состояние, вознаграждение, действие} +
        # данные с лидара
        train_mtrx = []
        out_mtrx = []

        for var in train_data:
            train_mtrx.append(var[0])
            outpt = self.get_output(var[0], var[1])
            out_mtrx.append(outpt)
        self.network.train(np.array(train_mtrx), np.array(out_mtrx),
                           epochs=N)  # ([np.array(var[0])], [np.array(var[1])], epochs=N)
        # Программа должна дойти до этого места
        # НС завершила свое обучение
        print(self.network.errors)


    def get_output(self, inpt, condition):
        # condition = [new_state, action, reward]
        # Вычисление Q функции состояния s от НС
        q = self.get_predict_withcopynn(inpt)
        # Вычисление Q' функцкции состояния s' от НС
        q_new = self.get_output(inpt, condition[0])

        m_q1, m_q2, m_q3 = self.get_max_Q(q_new)

        # Пересчитывание Q с учетом reward
        reward = condition[2]

        q[condition[1][0]] = q[condition[1][0]] + self.alpha * (reward[0] + self.sigma * m_q1 - q[condition[1][1]])
        q[condition[1][1] + 3] = q[condition[1][1] + 3] + self.self.alpha * (reward[1] + self.sigma * m_q2 - q[condition[1][1] + 3])
        q[condition[1][2] + 6] = q[condition[1][1] + 6] + self.alpha * (reward[2] + self.sigma * m_q3 - q[condition[1][1] + 6])

        # q должно быть матрицей с обновленными значениями
        return q

    def get_max_Q(self, res):
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

        # act1, act2 и act3 указывают на действие с наибольшей оценкой
        return act1, act2, act3

    # Сохранение НС
    def save_nn(self):
        with open(self.file, 'wb') as f:
            dill.dump(self.network, file=f)

    # Открытие НС
    def open_nn(self):
        with open(self.file, 'rb') as in_strm:
            self.network = dill.load(in_strm)
            #return n_network
