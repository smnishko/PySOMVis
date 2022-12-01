# PySOMVis framework

**PySOMVis framework** involves popular Self-Organizing Maps visualization techniques, which is inspired by Java based **SOMToolbox** (http://www.ifs.tuwien.ac.at/dm/somtoolbox/index.html)
# Current visualizations 
Pictures bellow are based on the projected Chain Link Data set (http://ifs.tuwien.ac.at/dm/somtoolbox/datasets.html). It is synthetic data representing two intertwined rings, which presents the topology violations after projection.
</br> The SOM map represents **18x12 neurons** trained **10000 times** with learning rate **0.7** and sigma **7** in **SOMToolbox**.
<p align="center"></p>
<table align="center">
<tbody align="center">
  <tr align="center">
    <td align="center"><img src="PySOMVis/pics/git/activhist.png" width=100/></br><sup><sup>Activity Histogram</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/clustercon.png" width=100/></br><sup><sup>Cluster Connection</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/compplane.png" width=100/></br><sup><sup>Component Plane</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/dmatrix.png" width=100/></br><sup><sup>D-Matrix</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/toperror.png" width=100/></br><sup><sup>Topology Error</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/Umatrix.png" width=100/></br><sup><sup>U-Matrix</sup></sup></td>
  </tr>
  <tr align="center">
    <td align="center"><img src="PySOMVis/pics/git/graphbased.png" width=100/></br><sup><sup>Graph based</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/hithist.png" width=100/></br><sup><sup>Hit Histogram</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/metromap.png" width=100/></br><sup><sup>Metro Map</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/minimspantree.png" width=100/></br><sup><sup>Minimum Spanning Tree</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/Ustarmatrix.png" width=100/></br><sup><sup>U*-Matrix</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/piechart.png" width=100/></br><sup><sup>Pie Chart</sup></sup></td>
  </tr>
  <tr align="center">
    <td align="center"><img src="PySOMVis/pics/git/qerror.png" width=100/></br><sup><sup>Quantization Error</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/sdh.png" width=100/></br><sup><sup>Smoothed Data Histogram</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/skymeth.png" width=100/></br><sup><sup>Sky Metaphor</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/chessboard.png" width=100/></br><sup><sup>Chessboard</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/kmeans.png" width=100/></br><sup><sup>K-means (2 clusters)</sup></sup></td>
    <td align="center"><img src="PySOMVis/pics/git/agglomerative_clustering.png" width=100/></br><sup><sup>average, complete, single, WARD</sup></sup></td>
  </tr>
</tbody>
</table>
</br>

# SOMStreamVis approach
SOMStreamVis approach helps to explore dynamic pattern with trained map. The example represents weather forecast, it includes **5 features** of different temperature, pressure and wind speed values over **35 years** (taken from the https://power.larc.nasa.gov/data-access-viewer/).</br>
The features are following:
<ul>
  <li>RH2M - Relative Humidity at 2 Meters (%)</li>
  <li>PS - Surface Pressure (kPa)</li>
  <li>T2M - Temperature at 2 Meters (C)</li>
  <li>WS50M - Wind Speed at 50 Meters (m/s)</li>
  <li>ALLSKY_SFC8_LW_DWN - Downward Thermal Infrared (Longwave) Radiative Flux (kW-hr/m^2/day)</li>
  </ul>
Dynamic exploration with SOMStreamVis:

<p align="center"></p>
<table align="center">
<tbody align="center">
  <tr align="center">
    <td align="center"><img src="PySOMVis/pics/SOMStreamVis_i.png" width=550/></br><sup>SOMStreamVis interface with trajectory-based approach</sup></td>
    <td align="center"><img src="PySOMVis/pics/SOMStreamVis_3years.png" width=450/></br><sup>Projection of 3 years (coloring is based on WARD clusterisation)</sup></br><img src="PySOMVis/pics/35years_Taxis.png" width=450/></br><sup>Projection of 35 years (coloring is based on WARD clusterisation)</sup></td>
  </tr>
</tbody>
</table>

# Citation
<sub>1. Sergei Mnishko and Andreas Rauber. Som visualization framework in python, including somstreamvis, a time series visualization. In Jan Faigl, Madalina Olteanu, and Jan Drchal, editors, Advances in Self-Organizing Maps, Learning Vector Quantization, Clustering and Data Visualization, pages 98–107, Cham, 2022. Springer International Publishing. DOI: https://doi.org/10.1007/978-3-031-15444-7_10</sub>
