from abc import ABC, abstractmethod 
  
class VisualizationInterface(ABC):

	@abstractmethod
	def _activate_controllers(self): 
		pass

	@abstractmethod
	def _deactivate_controllers(self): 
		pass

	@abstractmethod
	def _calculate(self): 
		pass
