import numpy as np
from visualizations.iVisualization import VisualizationInterface
from visualizations.sdh import SDH
from controls.controllers import SkyMetaphorController
import holoviews as hv
import panel as pn
import scipy.ndimage


class SkyMetaphor(VisualizationInterface):

    def __init__(self, main):
        self._main = main
        self._controls = SkyMetaphorController(self._calculate, name='SkyMetaphor visualization')
        self._previous_color = ''

    def _activate_controllers(self, ):
        self._previous_color = self._main._maincontrol.colormap
        self._main._maincontrol.colormap = 'gist_gray'
        reference = pn.pane.Str("<ul><li>Sky-metaphor visualisation for self-organising maps.</b> Latif, K., Mayer, R. \"I-KNOW '07: 7th international conference on knowledge management.\" In Proc. of I-KNOW07, 2007, pp. 400-407, Graz, Austria</li></ul>")
        self._main._controls.append(pn.Column(self._controls, self._main._point_segment_options, reference))
        self._calculate(self._controls.smooth_factor, self._controls.pull_force)

    def _deactivate_controllers(self, ):
        self._main._pipe_paths.send([])
        self._main._maincontrol.colormap = self._previous_color
        self._main._pipe_points.send([])
    
    def normalize(self, values, actual_bounds, desired_bounds):
        return np.array([desired_bounds[0] + (x - actual_bounds[0]) * (desired_bounds[1] - desired_bounds[0]) / (actual_bounds[1] - actual_bounds[0]) for x in values])

    def _calculate(self, smooth_factor=None, lam=None):
        sdh,points = None, None
        if lam is not None:        
            k = 4
            points = np.empty((0,2))
            for vector in self._main._idata:
                dists = np.sqrt(np.sum(np.power(self._main._weights - vector, 2), axis=1))
                best_dists = np.argsort(dists)[0:k]
                xy_points =  np.array([[int(i%self._main._n), -1*int(i/self._main._n)+self._main._m] for i in best_dists])
                f = dists[best_dists[0]] / dists[best_dists[1:]]
                u1, ui = xy_points[0], xy_points[1:]
                
                use4points = 1
                if (ui[0][0] == ui[1][0] and ui[1][0] == ui[2][0]
                        or ui[0][1] == ui[1][1] and ui[1][1] == ui[2][1]):
                    use4points = 0        
                
                position = np.zeros(2, dtype="float64")
                for i in range(k - 1 - use4points):
                    if (ui[i][0] - u1[0]) != 0:
                        position[0] += f[i] * 1.0 / (ui[i][0] - u1[0])
                    if (ui[i][1] - u1[1]) != 0:
                        position[1] += f[i] * 1.0 / (ui[i][1] - u1[1])
                position = position*lam + u1
                points = np.vstack([points,position])
            
            points[:,0] = self.normalize(points[:,0], [0, self._main._n], [-0.5,0.5]) + 1/(self._main._n*2)
            points[:,1] = self.normalize(points[:,1], [0, self._main._m], [-0.5,0.5]) - 1/(self._main._m*2)

        if smooth_factor is not None:
            sdh = SDH.sdh(self._main._weights, self._main._m, self._main._n, self._main._idata, smooth_factor, 2)
            sdh = scipy.ndimage.zoom(sdh, 20, order=2)

        self._main._display(plot = sdh, points = points)

