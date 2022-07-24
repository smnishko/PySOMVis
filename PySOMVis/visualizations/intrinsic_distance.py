import numpy as np
import panel as pn
from visualizations.iVisualization import VisualizationInterface
from typing import Tuple, List
import numpy as np
from visualizations.graph import Graph
#------------------------------------------------------------------TESTING MODE-----------------------------------------------------------#
class IntrinsicDistance(VisualizationInterface):

    def __init__(self, main):
        self._main = main

    def _activate_controllers(self, ):
        reference = pn.pane.Str('Intrinsic Distance')
        self._main._controls.append(reference)
        self._calculate()

    def _deactivate_controllers(self):
        pass

    def _calculate(self):
        intrinsic_distance = np.zeros(self._main._m * self._main._n).reshape(self._main._m, self._main._n)
        quant_error = np.zeros(self._main._m * self._main._n).reshape(self._main._m, self._main._n)
        result_error_map = np.zeros(self._main._m * self._main._n).reshape(self._main._m, self._main._n)
        n_best_matching = np.zeros(self._main._n * self._main._m).reshape(self._main._m, self._main._n)

        for vector in self._main._idata:
            vec_to_weights_dis: np.ndarray = np.sqrt(np.sum(np.power(self._main._weights - vector, 2), axis=1)).reshape(self._main._m, self._main._n)
            idx_best: Tuple[int, int] = np.unravel_index(np.argmin(vec_to_weights_dis, axis=None), vec_to_weights_dis.shape)
            n_best_matching[idx_best] += 1
            #add quant error1
            quant_error[idx_best] += vec_to_weights_dis[idx_best]

            vec_to_weights_dis_wihtout_best: np.ndarray = np.copy(vec_to_weights_dis)
            vec_to_weights_dis_wihtout_best[idx_best] = np.amax(vec_to_weights_dis)
            idx_2nd_best: Tuple[int, int] = np.unravel_index(np.argmin(vec_to_weights_dis_wihtout_best, axis=None), vec_to_weights_dis_wihtout_best.shape)

            intrinsic_distance[idx_best] += self._calculate_distance(distances=vec_to_weights_dis, idx_best=idx_best, idx_2nd_best=idx_2nd_best)

        quant_error = quant_error # / n_best_matching
        result_error_map = quant_error + intrinsic_distance
        result_error_map[n_best_matching < 1] = 0.0
        self._main._display(plot=result_error_map)

    def _calculate_distance(self, distances: np.ndarray, idx_best: Tuple[int, int], idx_2nd_best: Tuple[int, int]) -> float:
        graph: Graph = Graph(self._generate_edges(distances))

        path: List[Tuple[int, int]] = graph.dijkstra(idx_best, idx_2nd_best)

        return sum([distances[vertex] for vertex in path])

    def _generate_edges(self, distances: np.ndarray) -> List[Tuple[Tuple[int, int], Tuple[int, int], float]]:
        edges = []
        n_col = distances.shape[0]
        n_row = distances.shape[1]
        for x in range(n_col):
            for y in range(n_row):
                if x < n_col - 1:
                    neighbor = (x + 1, y)
                    edges.append(((x, y), neighbor, distances[neighbor]))
                if x > 0:
                    neighbor = (x - 1, y)
                    edges.append(((x, y), neighbor, distances[neighbor]))

                if y < n_row - 1:
                    neighbor = (x, y + 1)
                    edges.append(((x, y), neighbor, distances[neighbor]))
                if y > 0:
                    neighbor = (x, y - 1)
                    edges.append(((x, y), neighbor, distances[neighbor]))

        return edges
