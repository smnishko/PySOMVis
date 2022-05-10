"""    
This Visualizer provides D-Matrix which is a special variant of U-Matrix.
        
"""

import numpy as np
import panel as pn
from visualizations.iVisualization import VisualizationInterface

class DMatrix(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
       
    def _activate_controllers(self, ):
        reference = pn.pane.Str('Distances based matrix.', )
        self._main._controls.append(reference)
        self._calculate()

    def _deactivate_controllers(self,):
        pass        

    def _calculate(self,):
        D=np.zeros(self._main._m*self._main._n)
        
        for i in range(self._main._m):
            for j in range(self._main._n):
                p = i*self._main._n+j
                region = []
                if j>0: region.append(p-1)
                if i>0: region.append(p-self._main._n)
                if j<self._main._n-1: region.append(p+1)
                if i<self._main._m-1: region.append(p+self._main._n)

                D[p] = np.median(np.linalg.norm(self._main._weights[region] - self._main._weights[p], axis=-1))      
        
        self._main._display(plot=D.reshape(self._main._m,self._main._n))