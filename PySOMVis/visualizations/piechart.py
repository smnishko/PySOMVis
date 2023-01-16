import numpy as np
from scipy.spatial import distance_matrix, distance
from visualizations.iVisualization import VisualizationInterface
import panel as pn
import holoviews as hv
from bokeh.palettes import Category20c, Category20
from bokeh.models import Legend, LegendItem

_COLOURS_93 = np.array(['#FF5555','#5555FF','#55FF55','#FFFF55','#FF55FF','#55FFFF','#FFAFAF','#808080',
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
              '#40FFFF','#C0C0C0','#800000','#000080'])


PIE_CHART = 0.05

class PieChart(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
       
    def _activate_controllers(self, ):

        if self._main._classes_names is not None:
            ColorColumn = pn.Column()
            for idx, name in enumerate(self._main._classes_names):
                ColorColumn.append(pn.widgets.ColorPicker(name=name, value=_COLOURS_93[idx], disabled=True))
            
        self._main._controls.append(ColorColumn) 
        self._calculate()

    def _deactivate_controllers(self,):
        self._main._pdmap[0] = self._main._Image * self._main._Paths       

    def _calculate(self,):
        grid = self._main._m * self._main._n
        n_classes = np.unique(self._main._classes).tolist()
        mapped_data = np.zeros(grid * len(n_classes)).reshape(grid,-1)

        bmu = np.apply_along_axis(lambda x: np.argmin( np.linalg.norm(
            self._main._weights - x.reshape((1, self._main._dim)), axis=1)), 1, self._main._idata)

        for i in range(len(self._main._classes)):
            c = n_classes.index(self._main._classes[i])
            u = bmu[i]
            mapped_data[u][c] += 1

        max_size = np.sum(mapped_data, axis=1).max()    
        pos_x, pos_y, radius, color = np.array([]), np.array([]), np.array([]), np.array([])
        start_angle, end_angle = np.array([]), np.array([])

        for p in range(mapped_data.shape[0]):
            nx, ny = self._main._convert_to_xy(neuron=p)
            a, b, c, d, e, f = self._get_pie_chart(nx, ny, mapped_data[p], max_size)
            pos_x       = np.append(pos_x,  a,axis=0)
            pos_y       = np.append(pos_y,  b,axis=0)
            color       = np.append(color,  c,axis=0)
            radius      = np.append(radius, d,axis=0)
            start_angle = np.append(start_angle,e,axis=0)
            end_angle   = np.append(end_angle,  f,axis=0)

        figure = hv.render(self._main._Image, backend='bokeh')
        figure.wedge(x=pos_x, y=pos_y, radius=radius, fill_color=color, start_angle=start_angle, end_angle=end_angle, line_color=[None]*len(radius))
        
#        items = []
#        indexes = [np.argmax(color==c) for c in np.unique(color)]
#        for i, ii in enumerate(indexes):
#            label = str(i)
#            if self._main._classes_names is not None: label = self._main._classes_names[i]
#            items.append(LegendItem(label = label, renderers=[figure.renderers[1]], index=(ii)))

#        legend = Legend(items=items)
#        figure.add_layout(legend, 'right')        

        self._main._pdmap[0] = figure        

    def _get_pie_chart(self, x, y, piechart, max_size):
        wedge = piechart > 0
        wedge_n = np.sum(wedge)
        if wedge_n > 0:
            total       = piechart[wedge].sum()
            angle       = piechart[wedge]/total * 2 * np.pi
            angle_start = np.insert(angle[:-1], 0, 0, axis=0)
            angle_end   = np.cumsum(angle)
            if len(wedge) >= 3:
                color   = _COLOURS_93[np.where(wedge==True)] #np.array(Category20[len(wedge)])[wedge]
            else:
                color   = _COLOURS_93[np.where(wedge==True)] #np.array(Category20[3][:len(wedge)])[wedge] 
            return np.array([x]*wedge_n), np.array([y]*wedge_n), color, np.array([total/max_size*PIE_CHART]*wedge_n), angle_start, angle_end, 
        return np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])