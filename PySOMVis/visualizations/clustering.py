"""    
This Visualizer provides clustering algorithm on top of neurons grid.
        
"""

import numpy as np
from visualizations.iVisualization import VisualizationInterface
from controls.controllers import ClusteringController
from sklearn.cluster import KMeans, AgglomerativeClustering
import panel as pn

class Clustering(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._controls = ClusteringController(self._calculate,  name = "Clustering visualization")
        
    def _activate_controllers(self, ):
        reference = pn.pane.Str("<ul><li><b>D. Merkl and A. Rauber.</b> \"Alternative ways for cluster visualization in self-organizing maps.\" In Proc. of the Workshop on Self-Organizing Maps (WSOM97), Helsinki, Finland, 1997.</li></ul>")
        self._main._controls.append(pn.Column(self._controls, reference, name=''))
        self._calculate(self._controls.approach)

    def _deactivate_controllers(self,):
        pass        

    def _calculate(self, method):
        if self._controls.approach == 0: self._KMeans()
        else:                            self._AgglomerativeClustering()

    def _KMeans(self,):
        kmeans = KMeans(n_clusters=self._controls.clusters).fit(self._main._weights)
        prediction = kmeans.labels_ 
        self._main._display(prediction.reshape(self._main._m, -1))

    def _AgglomerativeClustering(self,):
        agglo = AgglomerativeClustering(n_clusters=self._controls.clusters, linkage=self._controls.linkage_type) 
        prediction = agglo.fit_predict(self._main._weights)
        self._main._display(plot=prediction.reshape(self._main._m, -1))
