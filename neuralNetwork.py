from neupy import layers, algorithms, init
import dill
import numpy as np

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
        self.initialize()

    # Инициализация нейронной сети
    def initialize(self):
        self.network = algorithms.Momentum(
            [
                layers.Input(20),
                layers.Linear(20, weight=init.Uniform(-0.5, 0.5)) ,
                layers.LeakyRelu(15, weight=init.Uniform(-0.5, 0.5)),
                layers.LeakyRelu(15, weight=init.Uniform(-0.5, 0.5)),
                layers.LeakyRelu(12, weight=init.Uniform(-0.5, 0.5)),
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
