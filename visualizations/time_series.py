import numpy as np
from scipy.spatial import distance_matrix, distance
from visualizations.iVisualization import VisualizationInterface
from controls.controllers import TimeSeriesController
import panel as pn
import holoviews as hv
from holoviews.streams import Pipe, Buffer
import pandas as pd
import time
'd'
class TimeSeries(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._dfstream = Buffer(pd.DataFrame({'x': [], 'y': []}, columns=['x', 'y']), length=150, index=False)#
        self._controls = TimeSeriesController(self._calculate, self._clear, name = "Time Series")
        self._pipe_points = Pipe(data=[])

    def _activate_controllers(self, ):
        self._main._controls.append(pn.Column(self._controls)) 
        self._main._timeseries.append(hv.DynamicMap(hv.Points, streams=[self._dfstream]).opts(width=950, height=350,ylim=(-1, self._main._m*self._main._n), shared_axes=False))
        self._main._pdmap[0] = pn.Column(self._main._Image * hv.DynamicMap(hv.Points, streams=[self._pipe_points]).opts(color='Red', marker='+', size=30))

    def _deactivate_controllers(self,):
        self._main._timeseries.clear() 
        self._main._pdmap[0] = pn.Column(self._main._Image * self._main._Paths)       

    def _calculate(self, ):
        bmu = np.apply_along_axis(lambda x: np.argmin( np.linalg.norm(self._main._weights - x.reshape((1, self._main._dim)), axis=1)), 1, self._main._idata)
        for i, u in enumerate(bmu):
        	self._pipe_points.send(self._main._get_neuron_xy(u))
        	self._dfstream.send(pd.DataFrame([(i, u)], columns=['x', 'y']))
        	time.sleep(.1)
    
    def _clear(self,):
        self._dfstream.clear()
        self._pipe_points.send([])

    def _add_data(self, unit = None):
        u = np.clip(unit, 0, self._main._m * self._main._n - 1)
        i = self._dfstream.data.size + 1
        self._pipe_points.send(self._main._get_neuron_xy(u))
        self._dfstream.send(pd.DataFrame([(i, u)], columns=['x', 'y']))    	

