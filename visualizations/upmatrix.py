from visualizations.iVisualization import VisualizationInterface
from controls.controllers import UStar_PMatrixController
from visualizations.umatrix import UMatrix
import panel as pn
import numpy as np
class UStar_PMatrix(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._percentiles = self._calculatePercentiles()
        percentile = self.calculateParetoRadiusPercentile()
        radius = self._percentiles[percentile] 
        self._controls = UStar_PMatrixController(percentile, radius, self._calculate, self._calculate_optimal, self._percentiles, name='P-Matrix & U*-Matrix')
        self._controls.radius = radius
        self._controls.percentile = percentile

    def _activate_controllers(self, ):
        reference = pn.pane.Str("<ul><li><b>P-Matrix:</b> Ultsch, A. \"Maps for the Visualization of high-dimensional Data Spaces.\" In Proceedings Workshop on Self-Organizing Maps (WSOM 2003), Kyushu, Japan</li> <li><b>U*-Matrix:</b> Ultsch, A.  \"A Tool to visualize Clusters in high dimensional Data.\" Technical Report No. 36, Dept. of Mathematics and Computer Science, University of Marburg, Germany, 2003</li></ul>")
        self._main._controls.append(pn.Column(self._controls, reference, name = '')) #default_layout=pn.Row, 
        self._calculate()

    def _deactivate_controllers(self,):
        pass  

    def _calculate(self, ):
        distance = lambda v: np.sum(np.linalg.norm(self._main._idata[:, None, :] - v, axis=-1) < self._controls.radius)
        plot = np.array([distance(v) for v in self._main._weights])
        if self._controls.ustar_matrix: plot = self._calculate_ustar_matrix(plot)
        self._main._display(plot = plot.reshape(self._main._m, self._main._n))

    def _calculate_ustar_matrix(self, matrix):
        um = UMatrix.calculate_UMatrix(self._main._weights, self._main._m, self._main._n, self._main._dim)
        um = um[0::2,0::2].reshape(1,-1)[0] # u-matrix
        pm = matrix.reshape(1,-1)[0]   # p-matrix
        ustarm = []
        
        meanP = np.mean(pm);
        maxP  = np.max(pm);
        diff = meanP - maxP;
        
        n = pm.size
        for i in range(n):
            scaleFactor = (pm[i] - meanP) / diff + 1
            ustarm.append(um[i] * scaleFactor)
        
        return np.array(ustarm)

    def _calculate_optimal(self,):
        percentile = self.calculateParetoRadiusPercentile()
        radius = self._percentiles[percentile]
        return percentile, radius 

    def _calculatePercentiles(self,):
        #distance = np.linalg.norm(self._main._idata[:, None, :] - self._main._idata[None, :, :], axis=-1)
        #calculate quantile only for upper triangle of distance matrix
        #return np.quantile(distance[np.triu_indices(distance.shape[0], k = 1)], np.arange(0.01, 1.01, 0.01)) 
        return np.quantile(self._main._distance[np.triu_indices(self._main._distance.shape[0], k = 1)], np.arange(0.01, 1.01, 0.01)) 
    
    #calculate density for every unite
    def getAllDensities(self, radius):
        #distances = np.linalg.norm(self._main._idata[:, None, :] - self._main._idata[None, :, :], axis=-1)
        n = self._main._distance.shape[0]#distances.shape[0]
        return [np.sum(self._main._distance[i,i+1:n] < radius) for i in range(n)]
    
    def calculateParetoRadiusPercentile(self,):
        PARETO_SIZE = 0.2013

        percentile = 18

        last_percentile = percentile
        diff = 0.0
        last_diff = 1.0
        median_size = 0
        stop = False
        upper_size = 1.0
        lower_size = 0.0

        upper_percentile = 50
        lower_percentile = 2


        while (not stop):
            radius = self._percentiles[percentile]
            densities = self.getAllDensities(radius)
            if len(densities)>0:
                median_size = max(np.median(densities), np.mean(densities)) / (self._main._n * self._main._m);
            else:
                median_size = 0;
            diff = median_size - PARETO_SIZE

            stop = abs(percentile - last_percentile) == 1 or percentile == upper_percentile or percentile == lower_percentile
            if (not stop):
                last_percentile = percentile
                last_diff = diff
                if (diff > 0):
                    upper_percentile = percentile
                    upper_size = median_size
                else:
                    lower_percentile = percentile
                    lower_size = median_size
                pest = (PARETO_SIZE - lower_size) / (upper_size - lower_size) * (upper_percentile - lower_percentile) + lower_percentile
                step = pest - percentile
                if (step > 0): step = max(step, 1) 
                else:          step = min(step, -1)
                percentile = percentile + int(round(step))
            else:
                if (abs(diff) > abs(last_diff)): percentile = last_percentile

        return percentile