import numpy as np
import panel as pn
import pandas as pd
from controls.controllers import ClusterConnectionController
from visualizations.iVisualization import VisualizationInterface

class ClusterConnection(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._controls = ClusterConnectionController(self._calculate, name='Cluster connection')
        self._alpha = []
        self._old_coolormap = ''

    def _activate_controllers(self, ):
        reference = pn.pane.Str('<ul><li>"Alternative ways for cluster visualization in self-organizing maps." <b>Merkl, Dieter, and Andreas Rauber.</b> Proc Workshop on Self-Organizing Maps (WSOM97), Espoo, Finland</li></ul>')
        self._main._segmentoptions.color = 'black'
        self._main._segmentoptions.size = 5
        self._old_coolormap = self._main._maincontrol.colormap
        self._main._maincontrol.colormap = 'RdGy'
        self._main._display(plot=[])
        self._main._controls.append(pn.Column(self._controls, reference))
        self._get_paths()

    def _deactivate_controllers(self,):
        self._main._display(paths=[])
        self._main._maincontrol.colormap = self._old_coolormap
        self._main._segmentoptions.color = 'red'
        self._main._segmentoptions.size = 2

    def _calculate(self, paths, t1, t2, t3):
        new_alpha = paths if not paths is None else self._main._pipe_paths.data
        new_alpha.iloc[:,4] = 0

        mask = np.where(self._alpha > t2) and np.where(self._alpha < t3)
        if np.any(mask): new_alpha.iloc[mask[0],4] = 0.1

        mask = np.where(self._alpha > t1) and np.where(self._alpha < t2)
        if np.any(mask): new_alpha.iloc[mask[0], 4] = 0.45

        mask = self._alpha < t1
        if np.any(mask): new_alpha.iloc[mask, 4] = 1

        self._main._display(paths=new_alpha)

    def _get_paths(self,):
        paths = []
        for y in range(0, self._main._m):
            for x in range(0, self._main._n):
                n = self._idx(y,x)
                if n<(self._main._m * self._main._n-1):
                    if   y==self._main._m-1 and x<self._main._n-1:  self._add(paths, n, self._idx(y,  x+1))
                    elif x==self._main._n-1 and y<self._main._m-1:  self._add(paths, n, self._idx(y+1,x))
                    else:
                        self._add(paths, n, self._idx(y,  x+1))
                        self._add(paths, n, self._idx(y+1,x))
        
        self._alpha = np.array(paths)[:,4] #work only with alpha
        self._alpha = np.interp(self._alpha, (min(self._alpha), max(self._alpha)), (0, 2))
        self._calculate(pd.DataFrame(paths, columns=['x0','x1','y0','y1','alpha']), self._controls.t1, self._controls.t2, self._controls.t3)

    def _add(self, paths, n1, n2):
        w = np.linalg.norm(self._main._weights[n1] - self._main._weights[n2])
        xy1 = list(self._main._convert_to_xy(neuron=n1))
        xy2 = list(self._main._convert_to_xy(neuron=n2))

        l = 0.01
        if (xy1[0] == xy2[0]):
            xy1[1] -=  l
            xy2[1] +=  l
        else: 
            xy1[0] += l
            xy2[0] -= l

        paths.append(xy1+xy2+[w])

    def _idx(self, y, x): #get neuron's index from xy
        return np.ravel_multi_index((y,x), dims=(self._main._m, self._main._n))