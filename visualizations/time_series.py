import numpy as np
from scipy.spatial import distance_matrix, distance
from visualizations.iVisualization import VisualizationInterface
from controls.controllers import TimeSeriesController
import panel as pn
import holoviews as hv
from holoviews.streams import Pipe, Buffer
import pandas as pd
import time
from threading import Thread
from tkinter import *

class TimeSeries(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._dfstream = Buffer(pd.DataFrame({'time': [], 'neurons': [], 'color': []}, columns=['time', 'neurons', 'color']), length=1, index=False)#
        self._avarage_points = Buffer(pd.DataFrame({'time': [], 'neurons': []}, columns=['time', 'neurons']), length=1, index=False)#
        self._controls = TimeSeriesController(self._calculate, self._clear, self._dfstream, self._avarage_points, name = "Time Series")
        self._pipe_points = Pipe(data=[])
        self.stop = False
        self.line = []
    
    def thread(func):
        def wrapper(*args, **kwargs):
            current_thread = Thread(target=func, args=args, kwargs=kwargs)
            current_thread.start()
        return wrapper

    def _activate_controllers(self, ):
        self._main._controls.append(pn.Column(self._controls))
        cmin, cmax = self._main._pipe.data.min(), self._main._pipe.data.max()
        Points = hv.DynamicMap(hv.Points, streams=[self._dfstream]).apply.opts(color='color', cmap=self._main._maincontrol.param.colormap, clim=(cmin, cmax)) 
        Curve  = hv.DynamicMap(hv.Curve, streams=[self._avarage_points]).opts(color='red')
        self._main._timeseries.append((Points*Curve).opts(width=950, height=350, ylim=(-1, self._main._m*self._main._n)))
        self._main._pdmap[0] = pn.Column(self._main._Image * hv.DynamicMap(hv.Points, streams=[self._pipe_points]).opts(color='Black', marker='*', size=30))

    def _deactivate_controllers(self,):
        self._main._timeseries.clear() 
        self._main._pdmap[0] = pn.Column(self._main._Image * self._main._Paths)       
   
    @thread
    def _calculate(self, ):
        bmu = np.apply_along_axis(lambda x: np.argmin( np.linalg.norm(self._main._weights - x.reshape((1, self._main._dim)), axis=1)), 1, self._main._idata)
        matrix = self._main._pipe.data.reshape(-1,1) 
        for i, u in enumerate(bmu):
           self._pipe_points.send(self._main._get_neuron_xy(u))
           self._dfstream.send(pd.DataFrame(np.vstack([i, u, matrix[u]]).T, columns=['time', 'neurons', 'color']))
           ewa = 0.01*self._controls.betta*self._avarage_points.data.neurons.iloc[-1] + (1-0.01*self._controls.betta)*u if self._avarage_points.data.neurons.size>0 else u #Exponentially Weighted Averages
           self._avarage_points.send(pd.DataFrame([(i, ewa)], columns=['time', 'neurons']))
           time.sleep(self._controls.speed)
           if self.stop:
              self.stop = False
              break

    def _clear(self,):
        self.stop = True
        self._dfstream.clear()
        self._avarage_points.clear()
        self._pipe_points.send([])

    def _add_data(self, unit = None):
        u = np.clip(unit, 0, self._main._m * self._main._n - 1)
        i = self._dfstream.data.size + 1
        self._pipe_points.send(self._main._get_neuron_xy(u))
        self._dfstream.send(pd.DataFrame([(i, u)], columns=['time', 'neurons']))    	