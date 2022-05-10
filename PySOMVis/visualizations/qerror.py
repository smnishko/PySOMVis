"""

Visualization of some aspects of Quantization Error

"""

import numpy as np
from visualizations.iVisualization import VisualizationInterface
from controls.controllers import QErrorController
import panel as pn
from scipy.spatial import distance_matrix, distance

class QError(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._controls = QErrorController(self._calculate, name='Quantization Error')
       
    def _activate_controllers(self, ):
        self._main._controls.append(pn.Column(self._controls, name = ''))
        self._calculate(self._controls.approach)

    def _deactivate_controllers(self,):
        pass        

    def _calculate(self, approach):
        qerror = np.zeros(self._main._n * self._main._m)
        hits = np.zeros(self._main._n * self._main._m)
        
        for vector in self._main._idata:
            position =np.argmin(np.sqrt(np.sum(np.power(self._main._weights - vector, 2), axis=1)))
            qerror[position] += np.linalg.norm(vector - self._main._weights[position])
            hits[position] += 1
        #'qe' -  0
        #'mqe' - 
        if approach == 0:
            plot = qerror.reshape(self._main._m, self._main._n)
        else:
        	mqe = np.zeros(self._main._n * self._main._m)
        	for i in range(len(qerror)):
        		mqe[i] = qerror[i] / hits[i] if hits[i] != 0 else 0
        	plot = mqe.reshape(self._main._m, self._main._n)

        self._main._display(plot=plot)