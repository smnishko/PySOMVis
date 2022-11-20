from visualizations.iVisualization import VisualizationInterface
from controls.controllers import ComPlaneController
import panel as pn

class ComponentPlane(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._controls =  ComPlaneController(self._calculate, (0, self._main._dim-1), name='Component Planes')

    def _activate_controllers(self, ):
        reference = pn.pane.Str('Slicing weight vector according its components.', )
        self._main._controls.append(pn.Column(self._controls, reference, name='' ))
        self._calculate(self._controls.component)
        
    def _deactivate_controllers(self,):
        pass

    def _calculate(self, component):
        if self._main._component_names is not None: 
            self._main._controls[0][0][1].name = self._main._component_names[self._controls.component]
        
        plot = self._main._weights[:,component].reshape(self._main._m, self._main._n)
        self._main._display(plot=plot)