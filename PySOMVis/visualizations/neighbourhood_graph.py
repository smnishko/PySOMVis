
"""

This visualisation provides two visualization plugin-ins for neighbourhood graphs. 
The first one uses knn-based distances, the second one radius-based distances.
 
"""

import numpy as np
from visualizations.iVisualization import VisualizationInterface
from controls.controllers import NeighbourhoodGraphController
import panel as pn

class NeighbourhoodGraph(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._controls = NeighbourhoodGraphController(self._calculate, name="Neighbourhood Graph")
       
    def _activate_controllers(self, ):
        reference = pn.pane.Str("<ul><li><b>Georg Poelzlbauer, Andreas Rauber, and Michael Dittenbach.</b> <a href=\"http://www.ifs.tuwien.ac.at/~poelzlbauer/publications/Poe05ISNN.pdf\"> Advanced visualization techniques for self-organizing maps with graph-based methods.</a> In Jun Wang, Xiaofeng Liao, Zhang Yi, editors, Proceedings of the Second International Symposium on Neural Networks (ISNN'05), pages 75-80, Chongqing, China, May 30 - June 1 2005. Springer-Verlag. </li></ul>")
        self._main._controls.append(pn.Column(self._controls, reference, name=''))
        self._calculate(self._controls.approach)

    def _deactivate_controllers(self,):
        self._main._pipe_paths.send([])        

    def _calculate(self, method):
        if self._controls.approach == 0: self._neighbourhood_knn()
        else:                            self._neighbourhood_radius()

    def _neighbourhood_knn(self, ):
      
        bmu_array = np.apply_along_axis(lambda x: np.argmin( np.linalg.norm(self._main._weights - x.reshape((1, self._main._dim)), axis=1)), 1, self._main._idata)
        neighbours = np.argpartition(self._main._distance, self._controls.knn)[:,:self._controls.knn+1]

        points = set()
        for index, neighbour_idxs in enumerate(neighbours):
            for neighbour_idx in neighbour_idxs:
                if index > neighbour_idx: points.add((bmu_array[neighbour_idx], bmu_array[index]))
                if index < neighbour_idx: points.add((bmu_array[index], bmu_array[neighbour_idx]))
        
        paths = []
        for p in points:
            paths.append(self._main._convert_to_xy(neuron=p[0])+self._main._convert_to_xy(neuron=p[1]))

        self._main._display(paths=paths)

    def _neighbourhood_radius(self,):
        
        num_nodes = self._main._idata.shape[0]

        # for each input vector, get the assigned output unit (index), based on euclidean distance
        input_assigned_units = np.apply_along_axis(lambda x: np.argmin( np.linalg.norm(self._main._weights - x.reshape((1, self._main._dim)), axis=1)), 1, self._main._idata)

        filtered_by_radius = self._main._distance < self._controls.radius

        # remove loops in the arc (with distance = 0)
        np.fill_diagonal(filtered_by_radius, False)

        # remove upper diagonal of this matrix, as the edges are undirected
        filtered_by_radius_without_upper_triangle = np.tril(filtered_by_radius).astype(np.int)

        # we multiply an index matrix (0...n) with the boolean one, to obtain in each column vector a list of relevant unit indices
        index_matrix = np.array( [list(range(0, num_nodes)), ] * num_nodes).transpose()
        filtered_unit_index_matrix = np.multiply(filtered_by_radius_without_upper_triangle, index_matrix)

        # set irrelevant columns to -1
        result_matrix = np.where(filtered_unit_index_matrix > 0, filtered_unit_index_matrix, -1)


        # visualization: iterate through column vectors, obtain unit coordindates and insert into line set
        points = set()
        for i in range(0, num_nodes):
            unit = input_assigned_units[i]
            my_partners_filtered = np.where(result_matrix[:, i] > -1)

            for u in input_assigned_units[my_partners_filtered]:
                if unit != u:
                    points.add((u,unit)) if unit > u else points.add((unit,u))

        paths = []
        for p in points:
            paths.append(self._main._convert_to_xy(neuron=p[0])+self._main._convert_to_xy(neuron=p[1]))

        self._main._display(paths=paths)