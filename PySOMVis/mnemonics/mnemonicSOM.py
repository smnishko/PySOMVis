
import numpy as np
import panel as pn
import random as rd
import math
from visualizations.umatrix import UMatrix
from controls.controllers import MnemonicSOMController
import mnemonics.input_utils as input_utils
from visualizations.iVisualization import VisualizationInterface

class MnemonicSOM(VisualizationInterface):

    def __init__(self, main):
        self._main = main
        self._controls = MnemonicSOMController(self._calculate, name='Mnemonic SOM visualization')
        self.distance_matrix, self.units = [], []
        self._weights = []

    def _activate_controllers(self, ):
        reference = pn.pane.Str("Mnemonic SOM visualization")
        self._main._controls.append(pn.Column(self._controls, reference))       

    def _deactivate_controllers(self,):
        pass        

    def _calculate(self,):
        self._main._pipe.send([])
        active_unit_matrix, self.distance_matrix = input_utils.load_mnemonic_image(self._controls.siluette, 
            som_width = self._controls.N, som_height = self._controls.M)

        for x, line in enumerate(active_unit_matrix):
            unit_line = []
            for y, state in enumerate(line):
                if state == 1:
                    unit_line.append(SOMUnit(x, y, self._main._dim, 
                        initial_learning_rate = self._controls.initial_learning_rate, 
                        learning_rate_decay = self._controls.learning_rate_decay, 
                        initial_radius = self._controls.initial_radius, 
                        radius_decay = self._controls.radius_decay))
                else:
                    unit_line.append(None)
            self.units.append(unit_line)


        self._train()
        ret = []
        for x in range(len(self.units)):
            for y in range(len(self.units[0])):
                if self.units[x][y]: ret.append(self.units[x][y].get_weights())
                else:                ret.append(np.full(self._main._dim, 0))
        
        self._weights = np.array(ret)
        
        self._main._display(UMatrix.calculate_UMatrix(self._weights, self._controls.M, self._controls.N, self._main._dim))


    def _train(self, verbose=False):
        for epoch in range(1, self._controls.epochs+1):
            if verbose: print("training epoch: ", epoch, "                          ")
            input_set = self._main._idata.copy().tolist()

            while len(input_set) > 0:
                i = rd.randint(0, len(input_set)-1) # take random input
                vec = input_set.pop(i)
                best_unit = self._get_best_unit(vec) # find best unit
                for line in self.units: # adjust weights
                    for unit in line:
                        if unit:
                            unit.adjust_weights(vec, self._controls.epochs, self.distance_matrix, best_unit)
                if verbose: print("vectors left: ", len(input_set), "                          ", end = "\r")
        if verbose: print("")

    def _get_best_unit(self, input_vector):
        best_unit = None
        best_value = -1

        for line in self.units:
            for unit in line:
                if unit:
                    value = unit.calculate_distance(input_vector)
                    if best_value == -1 or value < best_value:
                        best_unit = unit
                        best_value = value
                    
        return best_unit

class SOMUnit:

    def __init__(self, x, y, input_lenght, initial_learning_rate = .1, learning_rate_decay = 10, initial_radius = 1, radius_decay = 10):
        self.weights = np.random.rand(input_lenght)
        self.x = x
        self.y = y

        self.initial_radius = initial_radius
        self.radius_decay = (radius_decay if radius_decay != 0 else 1)
        self.learning_rate_decay = (learning_rate_decay if learning_rate_decay != 0 else 1)
        self.initial_learning_rate = initial_learning_rate

    def calculate_distance(self, input_vector):
        return math.sqrt(np.sum((self.weights-input_vector)**2))

    def adjust_weights(self, input_vector, epoch, distance_matrix, best_unit):
        self.weights += self._learning_rate(epoch) * self._topological_distance(epoch, distance_matrix, best_unit) * (input_vector - self.weights)

    def _topological_distance(self, epoch, distance_matrix, best_unit):
        return math.exp(-(distance_matrix.get_distance_by_coords(self.x, self.y, best_unit.x, best_unit.y)**2)/(2 * self._neighborhood_size(epoch) **2))

    def _neighborhood_size(self, epoch):
        return self.initial_radius * math.exp(-(epoch)/(self.radius_decay))

    def _learning_rate(self, epoch):
        return self.initial_learning_rate * math.exp(-(epoch)/(self.learning_rate_decay))

    def get_weights(self):
        return self.weights        