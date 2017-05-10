import neupy
from neupy import layers, algorithms
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
                layers.Relu(40),
                layers.Relu(40),
                layers.Relu(25),
                layers.Linear(9),
            ],

            error='categorical_crossentropy',
            step=0.01,
            verbose=True,
            shuffle_data=True,

            momentum=0.99,
            nesterov=True,
        )

    # Вычисление Q значений
    def get_prediction(self, input):
        print()
        return [0, 2, 5, 5, 1, 0, 9, 10, 5]

    # Тренировка НС
    def training(self, train_data, N = 1):
        for var in train_data:
            self.network.train(np.array(var[0]), np.array(var[1]), epochs=N)
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
