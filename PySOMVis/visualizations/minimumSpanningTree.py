import networkx as nx
from networkx.algorithms import tree
from holoviews import dim
import numpy as np
import panel as pn
from controls.controllers import MinimumSpanningTreeController
from visualizations.iVisualization import VisualizationInterface

class MinimumSpanningTree(VisualizationInterface):
    
    def __init__(self, main):
        self._main = main
        self._controls = MinimumSpanningTreeController(self._calculate, name='Minimum Spanning Tree')
        self._activated_unites = np.zeros(self._main._m * self._main._n)
        self._old_coolormap = ''
            
    def _activate_controllers(self, ):
        reference = pn.pane.Str('<ul><li>"Visualising Clusters in Self-Organising Maps with Minimum SpanningTrees." <b>Mayer, Rudolf, and Andreas Rauber.</b> International Conference on Artificial Neural Networks. Springer, Berlin, Heidelberg, 2010.</li></ul>')
        self._old_coolormap = self._main._maincontrol.colormap
        self._main._maincontrol.colormap = 'RdGy'
        self._main._display(plot=[])
        self._main._controls.append(pn.Column(self._controls, self._main._point_segment_options, reference))
        self._calculate(self._controls.connection_type, self._controls.weighted_lines)

    def _deactivate_controllers(self,):
        self._main._pipe_paths.send([])         
        self._main._pipe_points.send([]) 
        self._main._maincontrol.colormap = self._old_coolormap 

    def _calculate(self, connection_type=0, weighted_lines=False):

        self._activated_unites = np.zeros(self._main._m * self._main._n)
        for vector in self._main._idata: 
            idx_best = np.argmin(np.linalg.norm(self._main._weights - vector, axis=1))
            self._activated_unites[idx_best] = 1
        self._activated_unites = np.argwhere(self._activated_unites>0).flatten()
        
        G = nx.Graph()

        if connection_type == 0: self._all_edges(G)
        if connection_type == 1: self._diagonal_edges(G)
        if connection_type == 2: self._direct_edges(G)
        if connection_type == 3: self._input_data_edges(G)

        MST = tree.minimum_spanning_edges(G, algorithm="prim", data=True)
        
        paths = []
        points = set()
        for n1, n2, w in MST:
            paths.append(list(self._main._convert_to_xy(neuron=n1)+self._main._convert_to_xy(neuron=n2))+[w['weight']])
            points.add(self._main._convert_to_xy(neuron=n1))
            points.add(self._main._convert_to_xy(neuron=n2))

        if self._controls.weighted_lines:
            paths = self._norm_line_width(paths)
        
        self._main._display(paths=paths, points = list(points) )


    def _all_edges(self, G):
        for v1 in range(0, len(self._main._weights)):
            for v2 in range(v1+1, len(self._main._weights)):
                self._add_edge(G, v1, v2)
    
    def _idx(self, y, x): #get neuron's index from xy
        return np.ravel_multi_index((y,x), dims=(self._main._m, self._main._n))

    def _input_data_edges(self, G):
        for v1 in range(0, len(self._main._idata)):
            for v2 in range(v1+1, len(self._main._idata)):
                distance = np.linalg.norm(self._main._idata[v1] - self._main._idata[v2])
                n1 = np.argmin(np.linalg.norm(self._main._weights - self._main._idata[v1], axis=1))
                n2 = np.argmin(np.linalg.norm(self._main._weights - self._main._idata[v2], axis=1))
                if (n1 != n2):
                    if G.get_edge_data(n1, n2):
                        if G.get_edge_data(n1, n2)['weight'] > distance:
                            G[n1][n2]['weight'] = distance
                    else:
                        G.add_edge(n1, n2, weight=distance)

    def _diagonal_edges(self, G):
        for y in range(0, self._main._m):
            for x in range(0, self._main._n):
                n = self._idx(y,x)
                if n<(self._main._m * self._main._n-1): #last neuron has all connections
                    if y==self._main._m-1 and x<self._main._n-1: self._add_edge(G, n, self._idx(y,  x+1))
                    elif x==0 and y<self._main._m-1:  
                        self._add_edge(G, n, self._idx(y,  x+1))
                        self._add_edge(G, n, self._idx(y+1,x+1))
                        self._add_edge(G, n, self._idx(y+1,x))
                    elif x==self._main._n-1 and y<self._main._m-1:
                        self._add_edge(G, n, self._idx(y+1,x))
                        self._add_edge(G, n, self._idx(y+1,x-1))
                    else:
                        self._add_edge(G, n, self._idx(y,  x+1))
                        self._add_edge(G, n, self._idx(y+1,x+1))
                        self._add_edge(G, n, self._idx(y+1,x))
                        self._add_edge(G, n, self._idx(y+1,x-1))

    def _direct_edges(self, G):
        for y in range(0, self._main._m):
            for x in range(0, self._main._n):
                n = self._idx(y,x)
                if n<(self._main._m*self._main._n-1):
                    if y==self._main._m-1 and x<self._main._n-1:    self._add_edge(G, n,self._idx(y,  x+1))
                    elif x==self._main._n-1 and y<self._main._m-1:  self._add_edge(G, n, self._idx(y+1,x))
                    else:
                        self._add_edge(G, n, self._idx(y,  x+1))
                        self._add_edge(G, n, self._idx(y+1,x))

    def _add_edge(self, G, n1, n2):
        is_activated_unit = lambda v1,v2: (v1 in self._activated_unites) and (v2 in self._activated_unites)  #if consider only activated unites
        distance          = lambda v1,v2 : np.linalg.norm(self._main._weights[v1] - self._main._weights[v2]) #calculate weight between two neurons

        if (not self._controls.only_activated) or (is_activated_unit(n1,n2)):
            G.add_edge(n1, n2, weight=distance(n1, n2))

    def _norm_line_width(self, paths):
        paths = np.array(paths)
        paths[:,4] = 1-paths[:,4]/paths[:,4].max()
        paths[:,4] = self._main._point_segment_options[1][2].value*paths[:,4]
        return paths