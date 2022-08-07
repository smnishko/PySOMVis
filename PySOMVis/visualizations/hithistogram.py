import numpy as np
import panel as pn
from scipy.spatial import distance_matrix, distance
from visualizations.iVisualization import VisualizationInterface

class HitHist(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
       
    def _activate_controllers(self, ):
        reference = pn.pane.Str('Mapped input vectors to weight vectors.')
        self._main._controls.append(reference)
        self._calculate()

    def _deactivate_controllers(self,):
        pass        

    def _calculate(self,):
        hist = np.zeros(self._main._m * self._main._n)
        for vector in self._main._idata: 
            position =np.argmin(np.sqrt(np.sum(np.power(self._main._weights - vector, 2), axis=1)))
            hist[position] += 1

        self._main._display(plot=hist.reshape(self._main._m, self._main._n))