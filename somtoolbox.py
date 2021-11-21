"""    Main class of SOM visualization
        
        This library tries to dublicate as much as possible of the SOM Toolbox 
        application from TU Vienna.

        Args:
          m (int): vertical number of neurons on the mxn grid.
          n (int): horizontal number of neurons on the mxn grid.
          dimension (numpy): vectore size of the SOM's weights.
          input_data (numpy): input data for projection on SOM grid.

        Returns:
          SOMVisualizaiton
"""

import panel as pn
import numpy as np
import holoviews as hv
from holoviews import opts
from holoviews.streams import Pipe, Buffer

from controls.controllers import MainController
hv.extension('bokeh')

from visualizations.complane import ComponentPlane
from visualizations.dmatrix import DMatrix
from visualizations.hithistogram import HitHist
from visualizations.sdh import SDH
from visualizations.qerror import QError
from visualizations.umatrix import UMatrix
from visualizations.upmatrix import UStar_PMatrix
from visualizations.neighbourhood_graph import NeighbourhoodGraph
from visualizations.clustering import Clustering
from visualizations.metromap import MetroMap
from visualizations.piechart import PieChart
from visualizations.chessboard import Chessboard
from visualizations.time_series import TimeSeries
from skimage.transform import resize

OBJECTS_CLASSES = [ComponentPlane, HitHist, UMatrix, DMatrix, UStar_PMatrix, 
                   SDH, PieChart, NeighbourhoodGraph, Chessboard, Clustering, 
                   MetroMap, QError, TimeSeries]

_COLOURS_93 = ['#FF5555','#5555FF','#55FF55','#FFFF55','#FF55FF','#55FFFF','#FFAFAF','#808080',
              '#C00000','#0000C0','#00C000','#C0C000','#C000C0','#00C0C0','#404040','#FF4040',
              '#4040FF','#40FF40','#FFFF40','#FF40FF','#40FFFF','#C0C0C0','#800000','#000080',
              '#008000','#808000','#800080','#008080','#FF8080','#8080FF','#80FF80','#FFFF80',
              '#FF80FF','#80FFFF','#FF5555','#5555FF','#55FF55','#FFFF55','#FF55FF','#55FFFF',
              '#FFAFAF','#808080','#C00000','#0000C0','#00C000','#C0C000','#C000C0','#00C0C0',
              '#404040','#FF4040','#4040FF','#40FF40','#FFFF40','#FF40FF','#40FFFF','#C0C0C0',
              '#800000','#000080','#008000','#808000','#800080','#008080','#FF8080','#8080FF',
              '#80FF80','#FFFF80','#FF80FF','#80FFFF','#FF5555','#5555FF','#55FF55','#FFFF55',
              '#FF55FF','#55FFFF','#FFAFAF','#808080','#C00000','#0000C0','#00C000','#C0C000',
              '#C000C0','#00C0C0','#404040','#FF4040','#4040FF','#40FF40','#FFFF40','#FF40FF',
              '#40FFFF','#C0C0C0','#800000','#000080']

class SOMToolbox():

    def __init__(self, m, n, dimension, weights, input_data=None, classes=None, component_names=None):
        
        self._height = self._width = 500
        self._pipe = Pipe(data=[])
        self._pipe_paths = Pipe(data=[])
        self._visualizations = []


        self._m = m
        self._n = n
        self._weights = weights
        self._dim = dimension
        self._idata = input_data
        if input_data is not None:
            self._distance = np.linalg.norm(self._idata[:, None, :] - self._idata[None, :, :], axis=-1)
        if classes is not None: self._classes = classes.astype(int) 
        else:       self._classes = classes
        self._component_names = component_names

        self._plot = None
        self._maincontrol = MainController(self._interpolation, self._rotate, self._visualizations, OBJECTS_CLASSES, name='')
        self._mainp = pn.Column(pn.panel(self._maincontrol, default_layout=pn.Row, width=700))

        self._xlim = (-.5*self._m/self._n,.5*self._m/self._n) if self._m>self._n else (-.5,.5)
        self._ylim = (-.5*self._n/self._m,.5*self._n/self._m) if self._n>self._m else (-.5,.5)
        #_COLOURS_93
        self._Image = hv.DynamicMap(hv.Image, streams=[self._pipe]).apply.opts(cmap=self._maincontrol.param.colormap, 
            width=self._width, height=self._height, xlim=self._xlim, ylim=self._ylim)
        self._Paths = hv.DynamicMap(hv.Segments, streams=[self._pipe_paths]).apply.opts(line_width=1, color='red')
        
        self._pdmap = pn.Column(self._Image * self._Paths)

        self._controls = pn.Row()
        self._timeseries = pn.Row()
        self._mainview = pn.Column(pn.Column(self._mainp, pn.Row(self._pdmap, self._controls)), pn.Column(self._timeseries))
       
        self._visualizations.append(ComponentPlane(self))
        if input_data is not None: self._visualizations.append(HitHist(self))
        self._visualizations.append(UMatrix(self))
        self._visualizations.append(DMatrix(self))
        if input_data is not None:
            self._visualizations.append(UStar_PMatrix(self))
            self._visualizations.append(SDH(self))
            self._visualizations.append(PieChart(self))
            self._visualizations.append(NeighbourhoodGraph(self))
            self._visualizations.append(Chessboard(self))
            self._visualizations.append(Clustering(self))
            self._visualizations.append(MetroMap(self))
            self._visualizations.append(QError(self))
            self._visualizations.append(TimeSeries(self))     

        self._visualizations[0]._activate_controllers()
    
    def _rotate(self, k):
        if self._m!=self._n: #in case SOM's sides are not equal
            self._xlim, self._ylim = self._ylim, self._xlim
            self._pdmap[0] = pn.Column(self._Image.opts(xlim=self._xlim, ylim=self._ylim) * self._Paths)       
        
        self._plot = np.rot90(self._plot, k=k, axes=(1,0))
        
        paths_rotated = []
        paths_old = self._pipe_paths.data if type(self._pipe_paths.data)==list else [self._pipe_paths.data] #check if only 1 path
        for p in paths_old:
            if k>0:  paths_rotated.append((p[1], -1*p[0], p[3], -1*p[2])) #clockwise
            if k<0:  paths_rotated.append((-1*p[1], p[0], -1*p[3], p[2])) #counter clockwise

        self._pipe.send(np.rot90(self._pipe.data, k=k, axes=(1,0)))
        self._pipe_paths.send(paths_rotated)

    def _interpolation(self, ):
        if self._maincontrol.interpolation:
            self._pipe.send(resize(self._plot, (1000, 1000)))
        else:
            self._pipe.send(self._plot)

    def _get_neuron_xy(self, neuron):
        rotation = self._maincontrol._orientation%4
        
        if (rotation == 2 or rotation == 0): m, n = self._m, self._n 
        else:                                m, n = self._n, self._m
        
        i, j = neuron//n, neuron%n
        ir, jr = i, j                                 #if clockwise rotated 0

        if rotation==1: ir, jr = j,   self._m-i       #if clockwise rotated 90
        if rotation==2: ir, jr = self._m-i, self._n-j #if clockwise rotated 180
        if rotation==3: ir, jr = self._n-j, i         #if clockwise rotated 270
        
        diffx = 1/n if (rotation == 3 or rotation == 0) else -1/n
        diffy = 1/m if (rotation == 3 or rotation == 2) else -1/m
        
        x, y = -0.5 + diffx/2 + jr*(1/n), 0.5 + diffy/2 - ir*(1/m)
        return x, y

    def _from_xy_to_neuron(self, pos_xy):
        return int(pos_xy[0] * self._m + pos_xy[1])

    def _get_xy(self, p):
        rotation = self._maincontrol._orientation%4
        
        if (rotation == 2 or rotation == 0): m, n = self._m, self._n 
        else:                                m, n = self._n, self._m

        #if we want to scale into [b-a]: (b-a)*((x-min)/(max-min))+a
        scale = lambda a,b,x,minx,maxx: (b-a)*((x-minx)/(maxx-minx))+a

        x = scale(-0.5, 0.5, p[0], -0.5, n-0.5)    #-.45 + (.95/(n-.5))*(p[0]-0)
        y = scale(-0.5, 0.5, p[1], -0.5, m-0.5)   #-0.45 + ((0.5+0.45)/(m-0))*(p[1]-0)

        return [x,y]

    def _display(self, plot=None, paths=None):
        if plot is not None: 
            self._plot = np.rot90(plot, k=self._maincontrol._orientation, axes=(1,0))
            if self._maincontrol.interpolation: 
                self._pipe.send(resize(self._plot, (1000, 1000)))
            else:
                self._pipe.send(self._plot)
            
        if paths is not None:
            self._pipe_paths.send(paths)

    def _onbigscreen(self,):
        pn.serve(self._mainview) #, start=False, show=False