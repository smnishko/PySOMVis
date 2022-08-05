from typing import Tuple
import numpy as np
import panel as pn
from visualizations.iVisualization import VisualizationInterface
from controls.controllers import TopographicErrorController
#check
class TopographicError(VisualizationInterface):

    def __init__(self, main):
        self._main = main
        self._controls = TopographicErrorController(self._calculate, name='Topograhpic Error')

    def _activate_controllers(self, ):
        self._main._controls.append(pn.Column(self._controls, name=''))
        self._calculate(self._controls.neighborhood)

    def _deactivate_controllers(self,):
        pass

    def _calculate(self, neighborhood_type: int):
        """
        calculates the topographic error of the given input data on the given SOM.
        *neighborhood_type* defines if the neighborhood is a 4-unit neighbhorhood (von neumann neighborhood) or a 8-unit neighborhood (moore neighborhood)
        """

        topoerror = np.zeros(self._main._m * self._main._n)
        n_best_matching = np.zeros(self._main._m * self._main._n)
        n_2nd_best_not_neighbor = np.zeros(self._main._m * self._main._n)
        hist = np.zeros(self._main._m * self._main._n)

        for vector in self._main._idata:
            # calculate distance between current input vector and all units
            vec_to_weights_dis = np.linalg.norm(self._main._weights - vector, axis=1)#np.sqrt(np.sum(np.power(self._main._weights - vector, 2), axis=1))

            # extract first and 2nd best unit index
            idx_best = np.argmin(vec_to_weights_dis, axis=0)
            hist[idx_best] = 1
            vec_to_weights_dis[idx_best] = np.amax(vec_to_weights_dis)
            idx_2nd_best = np.argmin(vec_to_weights_dis, axis=0)

            pos_best = self._caclulate_position_from_index(idx_best)
            pos_2nd_best = self._caclulate_position_from_index(idx_2nd_best)

            n_best_matching[idx_best] += 1
            if not self._is_in_neighborhood(pos_best, pos_2nd_best, neighborhood_type):
                n_2nd_best_not_neighbor[idx_best] += 1

        units_with_error_mask = n_2nd_best_not_neighbor > 0
        topoerror[units_with_error_mask] = n_2nd_best_not_neighbor[units_with_error_mask]
        
        #display only mapped neurons 
        topoerror = topoerror.reshape(self._main._m, self._main._n) * hist.reshape(self._main._m, self._main._n) #np.rot90(hist.reshape(self._main._m, self._main._n))

        self._main._display(plot=topoerror)

    def _caclulate_position_from_index(self, index: int) -> Tuple[int, int]:
        """
        turns a given unit index into a 2D coordinate [col, row] on the current SOM
        """
        col = index // self._main._n
        row = index % self._main._n

        return col, row

    def _is_in_neighborhood(self, pos_unit: Tuple[int, int], pos_other_unit: Tuple[int, int], neighborhood_type: int) -> bool:
        """
        determines if *pos_other_unit* is in the neighorhood of *pos_unit*. 
        *neighborhood_type* defines if the neighborhood is a 4-unit neighbhorhood (von neumann neighborhood) or a 8-unit neighborhood (moore neighborhood)
        """

        row_dif = abs(pos_unit[1] - pos_other_unit[1])
        col_dif = abs(pos_unit[0] - pos_other_unit[0])

        if neighborhood_type == 4:  # 4-Unit Neighbhorhood
            return (row_dif == 0 and col_dif == 1) or (col_dif == 0 and row_dif == 1)
        elif neighborhood_type == 8:  # 8-Unit Neighbhorhood
            return row_dif <= 1 and col_dif <= 1

