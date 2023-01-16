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

from controls.controllers import MainController, PointOptions, SegmentOptions
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
from visualizations.somstreamvis import SOMStreamVis
from visualizations.sky_metaphor import SkyMetaphor
from visualizations.topographic_error import TopographicError
from visualizations.intrinsic_distance import IntrinsicDistance
from visualizations.activityhist import ActivityHist
from visualizations.minimumSpanningTree import MinimumSpanningTree
from visualizations.cluster_connection import ClusterConnection
from mnemonics.mnemonicSOM import MnemonicSOM
from skimage.transform import resize

OBJECTS_CLASSES = [ComponentPlane, HitHist, UMatrix, DMatrix, UStar_PMatrix, 
                   SDH, PieChart, NeighbourhoodGraph, Chessboard, Clustering, 
                   MetroMap, QError, SOMStreamVis, SkyMetaphor, TopographicError,
                   IntrinsicDistance, ActivityHist, MinimumSpanningTree, ClusterConnection, MnemonicSOM]

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

class PySOMVis():

    def __init__(self, weights, m=None, n=None, dimension=None, input_data=None, classes_names=None, classes=None, component_names=None):
        
        self._height = self._width = 500
        self._pipe = Pipe(data=[])
        self._pipe_points = Pipe(data=[])
        self._pipe_paths = Pipe(data=[])
        self._visualizations = []

        self._weights = weights
        #check ratio of the input map
        if len(self._weights.shape)==3 and m==None and n==None and dimension==None:
            self._m = self._weights.shape[0]
            self._n = self._weights.shape[1]
            self._dim = self._weights.shape[2]
            self._weights = self._weights.reshape(-1, self._dim)
        else:
            self._m = m
            self._n = n
            self._dim = dimension

        self._idata = input_data
        
        if input_data is not None:
            self._distance = np.linalg.norm(self._idata[:, None, :] - self._idata[None, :, :], axis=-1)
        
        if classes is not None: self._classes = classes.astype(int) 
        else:       self._classes = classes
        if component_names is not None: self._component_names = component_names
        else:                           self._component_names = None
        if classes_names is not None: self._classes_names = classes_names
        else:                         self._classes_names = None


        self._plot = None
        self._maincontrol = MainController(self._interpolation, self._rotate, self._flip, self._visualizations, OBJECTS_CLASSES, name='')
        self._pointoptions = PointOptions(name="Points")        
        self._segmentoptions = SegmentOptions(name="Segments")
        self._point_segment_options = pn.Tabs(self._pointoptions, self._segmentoptions)
        self._mainp = pn.Column(pn.panel(self._maincontrol, default_layout=pn.Row, width=700))

        self._xlim = (-.5*self._m/self._n,.5*self._m/self._n) if self._m>self._n else (-.5,.5)
        self._ylim = (-.5*self._n/self._m,.5*self._n/self._m) if self._n>self._m else (-.5,.5)
        #_COLOURS_93
        self._Image = hv.DynamicMap(hv.Image, streams=[self._pipe]).apply.opts(cmap=self._maincontrol.param.colormap, 
            width=self._width, height=self._height, xlim=self._xlim, ylim=self._ylim)
        self._Paths = hv.DynamicMap(hv.Segments, streams=[self._pipe_paths]).apply.opts(alpha='alpha', line_width=self._segmentoptions.param.size, 
                                                                                                                    color=self._segmentoptions.param.color)
        self._Points = hv.DynamicMap(hv.Points, streams=[self._pipe_points]).apply.opts(size=self._pointoptions.param.size, color=self._pointoptions.param.color,
                                                                                                                    marker=self._pointoptions.param.marker)
        
        self._pdmap = pn.Column(self._Image * self._Paths * self._Points)

        self._controls = pn.Row()
        self._somstreamvis = pn.Row()
        self._mainview = pn.Column(pn.Column(self._mainp, pn.Row(self._pdmap, self._controls)), pn.Column(self._somstreamvis))
       
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
            self._visualizations.append(SOMStreamVis(self))     
            self._visualizations.append(SkyMetaphor(self)) 
            self._visualizations.append(TopographicError(self)) 
            self._visualizations.append(IntrinsicDistance(self)) 
            self._visualizations.append(ActivityHist(self))

        self._visualizations.append(MinimumSpanningTree(self))
        self._visualizations.append(ClusterConnection(self))
        self._visualizations.append(MnemonicSOM(self))
        self._visualizations[0]._activate_controllers()
    
    def _rotate(self, k):
        self._weights = np.rot90(self._weights.reshape(self._m, self._n, self._dim), k).reshape(-1,self._dim)
        self._pipe.send(np.rot90(self._pipe.data, k))
        if self._m != self._n: 
            self._m, self._n = self._n, self._m
            self._ylim, self._xlim = self._xlim, self._ylim
            self._pdmap[0] = pn.Column(self._Image.opts(xlim=self._xlim, ylim=self._ylim) * self._Points * self._Paths)

    def _flip(self, horizontal):
        if horizontal:
            self._weights = np.fliplr(self._weights.reshape(self._m, self._n, self._dim)).reshape(-1,self._dim)
            self._pipe.send(np.fliplr(self._pipe.data))
        else:
            self._weights = np.flipud(self._weights.reshape(self._m, self._n, self._dim)).reshape(-1,self._dim)
            self._pipe.send(np.flipud(self._pipe.data))

    def _interpolation(self, ):
        if self._maincontrol.interpolation:
            self._pipe.send(resize(self._pipe.data, (1000, 1000)))

    def _convert_to_xy(self, neuron=None, point2D=None):
        scale = lambda a,b,x,minx,maxx: (b-a)*((x-minx)/(maxx-minx))+a  # adjust to -0.5 to 0.5 because of holoviews Image
        y, x = 0, 0
        if neuron is not None:   y, x = np.unravel_index(neuron, (self._m, self._n))
        if point2D is not None:  y, x = point2D[1], point2D[0]
        y = scale(-0.5, 0.5, y, -0.5, self._m-0.5)
        x = scale(-0.5, 0.5, x, -0.5, self._n-0.5)
        return x, -1*y

    def _display(self, plot=None, paths=None, points=None):
        if plot is not None: 
            if self._m==1:  plot = np.vstack([plot, plot])  # hv.Image doesn't work with one line input
            if self._n==1:  plot = np.c_[plot, plot]        # hv.Image doesn't work with one line input
            if self._maincontrol.interpolation: plot = resize(plot, (1000, 1000))
            self._pipe.send(plot)
        if paths is not None:
            self._pipe_paths.send(paths)
        if points is not None:
            self._pipe_points.send(points)

    def _onbigscreen(self,):
        pn.serve(self._mainview) #, start=False, show=False