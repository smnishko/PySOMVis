from visualizations.iVisualization import VisualizationInterface
from controls.controllers import SDHController
import panel as pn
import numpy as np

class SDH(VisualizationInterface):
    
    def __init__(self, main):
        self._main      = main
        self._controls  = SDHController(self._calculate, (1, self._main._m * self._main._n), name='Smoothed Data Histograms')
        self._reference = ["<ul><li><b>Smoothed Data Histograms:</b>  E. Pampalk, A. Rauber, and D. Merkl. \"Proceedings of the International Conference on Artificial Neural Networks (ICANN'02)\", pp 871-876, LNCS 2415, Madrid, Spain, August 27-30, 2002, Springer Verlag</li></ul>", "<br >Extension of Smoothed Data Histograms..<br>No rank is taken into account for histogram calculation, but distances between input vectors and weight vectors.", "<br >Extension of Smoothed Data Histograms.<br>No rank is taken into account for histogram calculation, but distances between input vectors and weight vectors.<br>Values are normalized per datum."]

    def _activate_controllers(self, ):
        ref =  self._reference[0]
        if self._controls.approach > 0: ref += self._reference[self._controls.approach]
        self._main._controls.append(pn.Column(self._controls, ref)) 
        self._calculate(self._controls.smoothing_factor, self._controls.approach)

    def _deactivate_controllers(self,):
        pass        

    def _calculate(self, factor, approach):
        import heapq
        
        sdh_m = np.zeros( self._main._m * self._main._n)

        cs=0
        for i in range(factor): cs += factor-i

        for vector in self._main._idata:
            dist = np.sqrt(np.sum(np.power(self._main._weights - vector, 2), axis=1))
            c = heapq.nsmallest(factor, range(len(dist)), key=dist.__getitem__)
            print(c)
            if (approach==0): 
                for j in range(factor):  sdh_m[c[j]] += (factor-j)/cs # normalized
                self._main._controls[0][1].object = self._reference[0]
            if (approach==1):
                for j in range(factor): sdh_m[c[j]] += 1.0/dist[c[j]] # based on distance
                self._main._controls[0][1].object = self._reference[0] + self._reference[1]
            if (approach==2): 
                dmin = min(dist[c])
                dmax = max(dist[c])
                for j in range(factor): sdh_m[c[j]] += 1.0 - (dist[c[j]]-dmin)/(dmax-dmin)
                self._main._controls[0][1].object = self._reference[0] + self._reference[2]
        
        plot = sdh_m.reshape(self._main._m, self._main._n)
        self._main._display(plot=plot)