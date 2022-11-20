import numpy as np
from scipy.spatial import distance_matrix, distance
from visualizations.iVisualization import VisualizationInterface
from controls.controllers import SOMStreamVisController
import panel as pn
import holoviews as hv
from holoviews.streams import Pipe, Buffer
import pandas as pd
import time
from threading import Thread
from tkinter import *

class SOMStreamVis(VisualizationInterface):
    
    def __init__(self, main):
        self._main     = main
        self._controls = SOMStreamVisController(self._calculate, self._get_projection, len(self._main._idata), name='SOMStreamVis')
        self._curve = Pipe(data=[])

    def _activate_controllers(self, ):
        self._main._controls.append(pn.Column(self._controls, self._main._point_segment_options))

        cmin, cmax = self._main._pipe.data.min(), self._main._pipe.data.max()
        bmu, curve = self._get_projection()

        Points = hv.Points(bmu, vdims='color').apply.opts(color='color', cmap=self._main._maincontrol.param.colormap, clim=(cmin, cmax), show_legend=False)#.opts(color='color', cmap=self._main._maincontrol.param.colormap, clim=(cmin, cmax))
        Curve  = hv.DynamicMap(hv.Curve, streams=[self._curve]).apply.opts(color='red', visible=self._controls.param.betta, 
                                            xlim=self._controls.param.Xrange, alpha=self._controls.param.betta,
                                            tools=['box_select','lasso_select'], framewise=True)

        self._main._somstreamvis.append((Points*Curve).opts(width=950, height=350, ylim=(-1, self._main._m*self._main._n), shared_axes=False))

    def _deactivate_controllers(self,):
        self._main._pipe_paths.send([])
        self._main._pipe_points.send([])        
        self._main._somstreamvis.clear() 
        self._main._pdmap[0] = pn.Column(self._main._Image * self._main._Paths * self._main._Points)
    
    def _get_projection(self,):
        bmu = np.apply_along_axis(lambda x: np.argmin( np.linalg.norm(self._main._weights - x.reshape((1, self._main._dim)), axis=1)), 1, self._main._idata)
        matrix = self._main._pipe.data.reshape(-1,1)
        curve, df = [bmu[0]], [] #pd.DataFrame(columns=['time', 'neurons', 'color'])
        for i,u in enumerate(bmu):
            df.append([i, u, float(matrix[u])])#pd.concat([df, pd.DataFrame([[i, u, str(matrix[u])]], columns=['time', 'neurons', 'color'])])
            #ewa = 0.9*curve[-1] + 0.1*u if len(curve)>0 else u
            ewa = (1-self._controls.betta_r)*curve[-1] + self._controls.betta_r*u if len(curve)>0 else u
            curve.append(ewa) #Exponentially Weighted Averages
        self._curve.send(curve)
        return df, curve

    def _calculate(self, ): 
        trajectory = []
        points = []
        if self._controls.projection != '-':
            borders = self._controls.Xrange 
            bmu = np.apply_along_axis(lambda x: np.argmin( np.linalg.norm(self._main._weights - x.reshape((1, self._main._dim)), axis=1)), 1, self._main._idata[int(borders[0]):int(borders[1])])
            trajectory = [self._main._convert_to_xy(neuron=bmu[i-1])+self._main._convert_to_xy(neuron=bmu[i]) for i in range(1, len(bmu))]
            points = [self._main._convert_to_xy(neuron=b) for b in bmu]
            if self._controls.projection == 'Points':     self._main._display(paths=[], points=points)
            else:                                         self._main._display(paths=trajectory, points=[])
        else:
            self._main._display(paths=[], points=[])