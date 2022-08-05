import numpy as np
import panel as pn
from controls.controllers import ActivityHistController
from visualizations.iVisualization import VisualizationInterface

class ActivityHist(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._controls = ActivityHistController(self._calculate, (0, len(self._main._idata)), name='Activity Histogram')

    def _activate_controllers(self, ):
        reference = pn.pane.Str("Sclising wight's vector accrodying it's components")
        self._main._controls.append(pn.Column(self._controls, reference))
        self._calculate(self._controls.idx_vec)        

    def _deactivate_controllers(self,):
        pass        

    def _calculate(self, vec_idx):
        vector = self._main._idata[vec_idx]
        activityHist = np.linalg.norm(self._main._weights - vector, axis=1)
        self._main._display(plot=activityHist.reshape(self._main._m,self._main._n))