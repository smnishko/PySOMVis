
from visualizations.iVisualization import VisualizationInterface
from scipy.spatial import Voronoi
from skimage.draw import polygon
from controls.controllers import ChessboardController
import holoviews as hv
import numpy as np
import panel as pn

class Chessboard(VisualizationInterface):
    
	def __init__(self, main):
		self._main = main
		self._controls = ChessboardController(self._calculate, name='Chessboard visualization')
     
	def _activate_controllers(self, ):
		reference = pn.pane.Str("<ul><li><b>Taha Abdel-Aziz</b> \"Coloring of the SOM based on Class Labels.\" Master Thesis, Department of Software Technology and Interactive Systems, Vienna University of Technology, October 2006.</li><li><b>Rudolf Mayer, Taha Abdel Aziz, and Andreas Rauber.</b> \"Visualising Class Distribution on Self-Organising Maps (accepted for publication).\" In Proceedings of the International Conference on Artificial Neural Networks (ICANN'07), Porto, Portugal, September 9- 13 2007. Springer Verlag.</li></ul>")
		self._main._controls.append(pn.Column(self._controls, reference))
		self._calculate()

	def _deactivate_controllers(self,):
		self._main._pipe_paths.send([])    

	def _calculate(self,):
		classes = [0] * (self._main._m * self._main._n)
		grid = self._main._m * self._main._n
		n_classes = np.unique(self._main._classes).tolist()
		mapped_data = np.zeros(grid * len(n_classes), dtype=int).reshape(grid,-1)

		bmu = np.apply_along_axis(lambda x: np.argmin( np.linalg.norm(
		    self._main._weights - x.reshape((1, self._main._dim)), axis=1)), 1, self._main._idata)

		for i in range(len(self._main._classes)):
		    c = n_classes.index(self._main._classes[i])
		    u = bmu[i]
		    mapped_data[u][c] += 1

		vpoints = []
		dummy=[]
		# position becomes a vpoint if it has a non-empty class array
		for position, v in enumerate(mapped_data):
		    if sum(v) > 0:
		        x,y = position % self._main._n, position // self._main._n
		        vpoints.append([x, y])

		        #dummy vetices for finit polygons
		        if x == 0:                        	  dummy.append([-1, y])
		        if x == self._main._n-1:              dummy.append([self._main._n, y])
		        if y == 0:                            dummy.append([x, -1])
		        if y == self._main._m-1:              dummy.append([x, self._main._m])
		        if x == 0 and y == 0:                 dummy.append([-1, -1])
		        if x == self._main._n-1 and y == self._main._m-1: 
		        	dummy.append([self._main._n, self._main._m])    
		        if x == self._main._n-1 and y == 0:   dummy.append([self._main._n, -1])
		        if x == 0 and y == self._main._m-1:   dummy.append([-1, self._main._m])
		            
		mapped_data = mapped_data[~np.all(mapped_data == 0, axis=1)]
		vpoints = dummy + vpoints

		# compute Voronoi tesselation
		vdiagram = Voronoi(vpoints)
		vdiagram.close() #release memory

		dpi = 100 if self._controls.high_dpi else 10

		get_vertices = lambda x: vdiagram.regions[vdiagram.point_region[x]]
		get_coordinates = lambda x: (vdiagram.vertices[x]+0.5)*dpi
		plot = np.zeros((self._main._n*dpi, self._main._m*dpi), dtype=int)

		for position in range(len(dummy), len(vpoints)):
		    polygon_cur = get_vertices(position)
		    poly = get_coordinates(polygon_cur)
		    rr, cc = polygon(poly[:,0], poly[:,1])
		    
		    #sometimes it is needed :) 
		    rr = rr[cc<plot.shape[1]]
		    cc = cc[cc<plot.shape[1]]
		    cc = cc[rr<plot.shape[0]]
		    rr = rr[rr<plot.shape[0]]
		    #end

		    colors = mapped_data[position-len(dummy)]
		    perc = np.round(colors/np.linalg.norm(colors,1.0), 3) # percentages (ratios) array
		    dominant_color = np.argmax(colors)
		    colors_ind = np.nonzero(mapped_data[position-len(dummy)])[0]
		    plot[rr,cc] = dominant_color
		    colors_ind = colors_ind[colors_ind!=dominant_color] #we don't need dominant color any more
		    if len(colors_ind) > 0:
		        pixels = np.column_stack((rr,cc))
		        total_pixels = len(pixels)
		        centroid = pixels.mean(0) #get center of the current region

		        if self._controls.chessboard:
		            np.random.shuffle(pixels)
		            chunks = np.split(pixels, (len(pixels)*perc[:-1].cumsum()).astype(int)) #split pixels accordingly percentages
		            for c, pixels  in enumerate(chunks):
		                plot[pixels[:,0],pixels[:,1]] = c 
		        else:
		            #find neighbours of current polygon
		            neighbours = vdiagram.ridge_points[(vdiagram.ridge_points==position).any(axis=1) 
		                                              & (vdiagram.ridge_points>=len(dummy)).all(axis=1)]
		            neighbours = neighbours[neighbours!=position].flatten() #remove the current region form neighbours

		            #get colors of all neighbors
		            neighbours_colors = np.insert(mapped_data[neighbours-len(dummy)], mapped_data.shape[1], neighbours, axis=1)
		            
		            for c in colors_ind: #go over all colors of polygon
		                pixels = pixels[plot[pixels[:,0],pixels[:,1]] == dominant_color] #we can change only pixels colored in dominant color
		                point1, point2 = None, None
		                
		                nc = neighbours_colors[neighbours_colors[:,c]>0] #check how many neighbours have the same colour
		                if   len(nc)==0: point1, point2 = centroid, None # color is isolated, no neighbours with the same color
		                elif len(nc)==1: # there is only one neighbour with the same color
		                    neighbour = get_vertices(nc[:,-1][0])
		                    adjacent_border = get_coordinates(np.intersect1d(polygon_cur, neighbour))
		                    
		                    #check if neighbor has only dominant color
		                    if (nc[nc>0].size-1==1): point1, point2 = adjacent_border[1], adjacent_border[0] #if this color is dominant color for neighbor - consider adjacent border
		                    else:                    point1, point2 = centroid, adjacent_border.mean(0)      #else consider line segment from center to border
		                        
		                elif len(nc)>1: #if we have a set of neighbours with the same color
		                   
		                    dominant = []
		                    not_dominant = []
		                    for n in nc: #divide set on dominant and not
		                        if n[n>0].size-1==1: dominant.append(n[-1])
		                        else:                not_dominant.append(n[-1])
		                    
		                    if len(dominant)>0: #consider dominant color of neighbors - first
		                        intersection = self._check_polygon_intersection(dominant, get_vertices)
		                        if intersection is not None: #check iintersection of neighbors with the same color
		                            point1, point2 = get_coordinates(intersection[0]), None
		                        else:
		                            neighbour = get_vertices(dominant[0]) # no intersection - take first neighbour
		                            adjacent_border = get_coordinates(np.intersect1d(polygon_cur, neighbour))
		                            point1, point2 = adjacent_border[0], adjacent_border[1]                      
		                    else: #same for neighbours which have the same color but not dominant
		                        intersection = self._check_polygon_intersection(not_dominant, get_vertices)
		                        if intersection is not None:
		                            point1 = get_coordinates(np.intersect1d(intersection[1],polygon_cur)).mean(0)
		                            point2 = get_coordinates(np.intersect1d(intersection[2],polygon_cur)).mean(0)
		                        else:
		                            neighbour1 = get_vertices(not_dominant[0])
		                            neighbour2 = get_vertices(not_dominant[-1])
		                            point1 = get_coordinates(np.intersect1d(neighbour1,polygon_cur)).mean(0)
		                            point2 = get_coordinates(np.intersect1d(neighbour2,polygon_cur)).mean(0)
		                    
		                sorted_pixels = self._dist_point_to_segment(pixels, point1, point2)
		                                
		                N = round(total_pixels*perc[c]) #get number of pixels accordying to the percentge
		                plot[sorted_pixels[0:N,0],sorted_pixels[0:N,1]] = c #cahnge pixel color
		
		paths = []
		if self._controls.voronoi_lines:
			for v in vdiagram.ridge_vertices:
				if -1 not in v:
					p1 = list(self._main._convert_to_xy(point2D=vdiagram.vertices[v[0]]))
					p2 = list(self._main._convert_to_xy(point2D=vdiagram.vertices[v[1]]))
					paths.append(tuple(p1)+tuple(p2))

		plot = np.flipud(np.rot90(plot, k=-1, axes=(1,0)))
		self._main._display(plot=plot, paths=paths)

	def _dist_point_to_segment(self, pixels, s0, s1=None):
	    """
	    Get the distance of a point to a segment or point.
	      *p*, *s0*, *s1* are *xy* sequences
	    This algorithm is from http://geomalgorithms.com/a02-_lines.html
	    """
	    distances = []
	    if s1 is None: #distance between points and point
	        distances = np.linalg.norm(pixels[:, None, :] - s0, axis=-1)
	    else:          #distance between point and line segment
	        dist = lambda x,y: round(np.linalg.norm(x-y),1)
	        for p in pixels:        
	            v,   w = s1 - s0, p - s0
	            c1, c2 = np.dot(w, v), np.dot(v, v)
	            b = c1 / c2
	            pb = s0 + b * v
	            if c1 <= 0:    distances.append(dist(p,s0))
	            elif c2 <= c1: distances.append(dist(p,s1))
	            else:          distances.append(dist(p,pb))
	    distances = np.column_stack((pixels,distances))
	    distances = distances[distances[:, -1].argsort()] #sort distances
	    return distances[:,0:2].astype(int)

	def _check_polygon_intersection(self, polygons, get_vertices):
	    """
	    Return shared vertex between polygons

	    """
	    for i in range(len(polygons)):
	        for j in range(i+1,len(polygons)): 
	            poly1 = get_vertices(polygons[i])
	            poly2 = get_vertices(polygons[j])
	            shared_vertex = np.intersect1d(poly1, poly2)
	            if shared_vertex.size==1: return (shared_vertex, poly1, poly2)
	    return None