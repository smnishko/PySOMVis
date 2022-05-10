"""    
U-matrix visualization
        
Implementation of the classic U-Matrix as described in 
Ultsch, A., and Siemon, H.P. 
"Kohonen's Self-Organizing Feature Maps for Exploratory Data Analysis."
In Proc. Intern. Neural Networks, 1990, pp. 305-308, Kluwer  Academic Press, Paris, France.

"""


from visualizations.iVisualization import VisualizationInterface
import numpy as np
import panel as pn

class UMatrix(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
       
    def _activate_controllers(self, ):
        reference = pn.pane.Str("<ul><li><b>U-Matrix:</b> Ultsch, A., and Siemon, H.P. \"Kohonen's Self Organizing Feature Maps for Exploratory Data Analysis.\" In Proc. Intern. Neural Networks, 1990, pp. 305-308, Kluwer Academic Press, Paris, France.</li></ul>")
        self._main._controls.append(reference)
        self._calculate()

    def _deactivate_controllers(self,):
        pass  

    def _calculate(self, ):
        U = UMatrix.calculate_UMatrix(self._main._weights, self._main._m, self._main._n, self._main._dim)
        self._main._display(plot=U)

    @staticmethod
    def calculate_UMatrix(weights, m, n, dim):
        U = weights.reshape(m, n, dim)
        U = np.insert(U, np.arange(1, n), values=0, axis=1)
        U = np.insert(U, np.arange(1, m), values=0, axis=0)
        #calculate of interpolation
        for i in range(U.shape[0]): 
            if i%2==0:
                for j in range(1,U.shape[1],2):
                    U[i,j][0] = np.linalg.norm(U[i,j-1] - U[i,j+1], axis=-1)
            else:
                for j in range(U.shape[1]):
                    if j%2==0: 
                        U[i,j][0] = np.linalg.norm(U[i-1,j] - U[i+1,j], axis=-1)
                    else:      
                        U[i,j][0] = (np.linalg.norm(U[i-1,j-1] - U[i+1,j+1], axis=-1) + np.linalg.norm(U[i+1,j-1] - U[i-1,j+1], axis=-1))/(2*np.sqrt(2))

        U = np.sum(U, axis=2) #move from Vector to Scalar

        for i in range(0, U.shape[0], 2): #count new values
            for j in range(0, U.shape[1], 2):
                region = []
                if j>0: region.append(U[i][j-1]) #check left border
                if i>0: region.append(U[i-1][j]) #check bottom
                if j<U.shape[1]-1: region.append(U[i][j+1]) #check right border
                if i<U.shape[0]-1: region.append(U[i+1][j]) #check upper border
                
                U[i,j] = np.median(region)

        return U