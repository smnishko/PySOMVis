import param
import numpy as np
from bokeh.palettes import Greys256

OBJECTS_ALL = {'Component Planes': 0, 'Hit Histogram': 1, 'U-matrix': 2, 'D-Matrix': 3,  
               'P-matrix & U*-matrix': 4, 'Smoothed Data Histograms': 5, 'Pie Chart': 6, 
               'Neighbourhood Graph': 7, 'Chessboard': 8, 'Clustering': 9, 'Metro Map': 10, 
               'Quantization Error': 11,  'Time Series': 12} 

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

PALETTES = ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral',
           'coolwarm', 'bwr', 'seismic', 'gist_gray', 'bone', 'pink', 'spring', 'summer',
           'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper','Greys',
           'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd',
           'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn','viridis', 'plasma',
           'inferno', 'magma', 'cividis','twilight', 'twilight_shifted', 'hsv','Pastel1', 'Paired',
           'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'flag',
           'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
           'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar','glasbey_dark']

class MainController(param.Parameterized):
    
    visualization = param.ObjectSelector(default=0, objects=OBJECTS_ALL, label='')
    colormap = param.ObjectSelector(default='jet', objects=PALETTES, label='')

    rotate_r = param.Action(lambda x: x.param.trigger('rotate_r'), label='↩')
    rotate_l = param.Action(lambda x: x.param.trigger('rotate_l'), label='↪')
    #flip_h   = param.Action(lambda x: x.param.trigger('flip_h'),   label='↔')
    #flip_v   = param.Action(lambda x: x.param.trigger('flip_v'),   label='↕')
    interpolation   = param.Boolean(False, label='interpolation')

    def __init__(self, interpolation, rotate, visualizations, vis_classes,  **params):
        super(MainController, self).__init__(**params)
        self._visualizations = visualizations
        self._vis_classes = vis_classes
        self._previous_vis = self.visualization
        self._orientation = 0
        self._interpolation = interpolation
        self._rotate = rotate
    
    
    @param.depends("interpolation", watch=True)
    def _interpolation(self):
        self._interpolation()

    @param.depends("rotate_r", watch=True)
    def _rotate_r(self):
        self._rotate(1)
        self._orientation += 1

    @param.depends("rotate_l", watch=True)
    def _rotate_l(self):
        self._orientation -= 1
        self._rotate(-1)

    #@param.depends("flip_h", watch=True)
    #def _flip_h(self):
    #    self._pipe.send(np.fliplr(self._pipe.data)) 
        
    #@param.depends("flip_v", watch=True)
    #def _flip_v(self):
    #    self._pipe.send(np.flipud(self._pipe.data))
        
    @param.depends("visualization", watch=True)
    def _change_app(self,):
        for a in self._visualizations:
            if isinstance(a, self._vis_classes[self._previous_vis]):
                a._main._controls.clear()
                a._deactivate_controllers()
        self._previous_vis = self.visualization
        for a in self._visualizations:
            if isinstance(a, self._vis_classes[self.visualization]):
                a._activate_controllers()

class ComPlaneController(param.Parameterized):
    
    component = param.Integer(0, bounds=(0, 0))
    
    def __init__(self, calculate, bounds, **params):
        super(ComPlaneController, self).__init__(**params)
        self.param.component.bounds = bounds
        self._calculate = calculate
    
    @param.depends("component", watch=True)
    def _change_data(self,):
        self._calculate(self.component) 

class SDHController(param.Parameterized):

    APPROACHES = {'SDH': 0, 'Weighted SDH': 1, 'Weighted SDH (norm.)': 2}

    approach = param.ObjectSelector(default=0, objects=APPROACHES)
    smoothing_factor   = param.Integer(5, bounds=(1, 7))

    def __init__(self, calculate, bounds, **params):
        super(SDHController, self).__init__(**params)
        self.param.smoothing_factor.bounds = bounds
        self._calculate = calculate
    
    @param.depends("smoothing_factor", 'approach', watch=True)
    def _change_data(self,):
        self._calculate(self.smoothing_factor, self.approach)

class QErrorController(param.Parameterized):

    APPROACHES = {'Quantization error': 0, 'Mean quantization error': 1}
    approach = param.ObjectSelector(default=0, objects=APPROACHES)
    
    def __init__(self, calculate,  **params):
        super(QErrorController, self).__init__(**params)
        self._calculate = calculate
    
    @param.depends("approach", watch=True)
    def _change_data(self,):
        self._calculate(self.approach)

class UStar_PMatrixController(param.Parameterized):

    percentile    = param.Integer(0, bounds=(0, 100))
    radius        = param.Number(0, bounds=(0, None))
    optimal_r     = param.Action(lambda x: x.param.trigger('optimal_r'), label='optimal')
    ustar_matrix  = param.Boolean(False, label='U*-Matrix')

    def __init__(self, percentile, radius, calculate, calculate_optimal, percentiles,  **params):
        super(UStar_PMatrixController, self).__init__(**params)
        self._calculate = calculate
        self._calculate_optimal = calculate_optimal
        self._percentiles = percentiles


    @param.depends("optimal_r", watch=True)
    def _calculate_optimal_radius(self):
        self.percentile, self.radius = self._calculate_optimal()
        self._change_radius()

    @param.depends("radius", watch=True)
    def _change_radius(self,):
        self._calculate()            

    @param.depends("percentile", watch=True)
    def _change_density(self,):
        self.radius = self._percentiles[self.percentile] 
        self._change_radius()

    @param.depends("ustar_matrix", watch=True)
    def _activate_ustarmatrix(self,):
        self._calculate() 

class NeighbourhoodGraphController(param.Parameterized):

    APPROACHES = {'Knn': 0, 'Radius': 1}

    approach  = param.ObjectSelector(default=0, objects=APPROACHES)
    knn       = param.Integer(1, bounds=(1, None))
    radius    = param.Number(0.1, bounds=(0.1, None), constant=True)

    def __init__(self, calculate,  **params):
        super(NeighbourhoodGraphController, self).__init__(**params)
        self._calculate = calculate


    @param.depends("approach", "knn", "radius", watch=True)
    def _change_approach(self,):
        if self.approach == 1:
            self.param['knn'].constant = True
            self.param['radius'].constant = False
        if self.approach == 0:
            self.param['knn'].constant = False
            self.param['radius'].constant = True
        self._calculate(self.approach)

class ClusteringController(param.Parameterized):
 
    APPROACHES = {'KMeans': 0, 'Agglomerative clustering': 1}
    LINKAGE_TYPES = {'single': 'single', 'complete':'complete', 'ward': 'ward', 'average':'average'}

    approach     = param.ObjectSelector(default=0, objects=APPROACHES)
    linkage_type = param.ObjectSelector(default='single', objects=LINKAGE_TYPES)
    clusters     = param.Integer(2, bounds=(2, None))

    def __init__(self, calculate,  **params):
        super(ClusteringController, self).__init__(**params)
        self._calculate = calculate


    @param.depends("approach", "clusters", "linkage_type", watch=True)
    def _change_approach(self,):
        if self.approach == 0: self.param['linkage_type'].constant = True
        else:                  self.param['linkage_type'].constant = False
                       
        self._calculate(self.approach)

class MetroMapController(param.Parameterized):

    stops            = param.Integer(3, bounds=(3, None), label='Number of bins')
    components_int   = param.ListSelector(default=[], objects=[], precedence=-1)
    components       = param.ListSelector(default=[], objects=[])
    snapping         = param.Boolean(False, label='Snap lines')
    level            = param.Number(0.3, bounds=(0.0, 1))
    water_level      = param.List(precedence=-1)

    def __init__(self, calculate, dim, component_names, **params):
        super(MetroMapController, self).__init__(**params)
        self._calculate = calculate
        self.water_level = [0, self.level, 1]
        self.param.components_int.objects = [i for i in range(dim)]
        if component_names is not None: self.param.components.objects = component_names
        else:                           self.param.components.objects = [str(i) for i in range(dim)]              
        self.components_int = [0]
    
    @param.depends("components", watch=True)
    def _change_components(self,):
        self.components_int = [self.param.components.objects.index(name) for name in self.components]
        self._calculate(False)

    @param.depends("snapping", watch=True)
    def _change_lines(self,):
        self._calculate(False)

    @param.depends("stops", watch=True)
    def _change_stops(self,):
        self._calculate(True)

    @param.depends("level", watch=True)
    def _change_water_level(self,):
        self.water_level = [0, self.level, 1]

class ChessboardController(param.Parameterized):

    chessboard    = param.Boolean(True, label='Chessboard')
    voronoi_lines = param.Boolean(True, label='Voronoi lines')
    high_dpi      = param.Boolean(False, label='High DPI')

    def __init__(self, calculate,  **params):
        super(ChessboardController, self).__init__(**params)
        self._calculate = calculate

    @param.depends("chessboard", "voronoi_lines", "high_dpi", watch=True)
    def _change_parameters(self,):
        self._calculate()
        
class TimeSeriesController(param.Parameterized):
    
    window_size = param.Integer(10,  bounds=(1, None))
    speed       = param.Number(0.1)
    betta       = param.Number(90.00, bounds=(0, 100))
    play        = param.Action(lambda x: x.param.trigger('play'), label='▶')
    clear       = param.Action(lambda x: x.param.trigger('clear'), label='■')

    def __init__(self, calculate, clear, _streams,_avarage_points,  **params):
        super(TimeSeriesController, self).__init__(**params)
        self._calculate = calculate
        self._clear = clear
        self._streams = _streams
        self._avarage_points = _avarage_points

    @param.depends("window_size", watch=True)
    def _change_length(self):
        self._streams.length = self.window_size
        self._avarage_points.length = self.window_size

    @param.depends("play", watch=True)
    def _play(self):
        self._calculate()

    @param.depends("clear", watch=True)
    def _clear(self):
        self._clear()