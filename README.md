# PySOMVis

This repository contains the result of Master Thesis paper in Technical University of Vienna. It envolvs popular Self-Organizing maps visualization techniques, which were taken from Java based SOMToolbox (http://www.ifs.tuwien.ac.at/dm/somtoolbox/index.html) and additional one which tries to follow the changes in Time Serries data set.<br>
The picture bellow (timeseries.ipynb) represents visualiztion algorithm on weather forecast data. The data set includes 5 fetures of different temperature, pressure and wind speed values over 35 years (taken from the https://power.larc.nasa.gov/data-access-viewer/). The features are following:
<ul>
  <li>RH2M - Relative Humidity at 2 Meters (%)</li>
  <li>PS - Surface Pressure (kPa)</li>
  <li>T2M - Temperature at 2 Meters (C)</li>
  <li>WS50M - Wind Speed at 50 Meters (m/s)</li>
  <li>ALLSKY_SFC8_LW_DWN - Downward Thermal Infrared (Longwave) Radiative Flux (kW-hr/m^2/day)</li>
  </ul>
 Here we can observ the 3 years forecast projection
<p align="center"><img src="PySOMVis/pics/SOM_TimeSerries.PNG" width=550/>
</br>The following plot represents projection over all dataset.</br>
<img src="PySOMVis/pics/35years_Taxis.png" width=550/></p>
 
 # Current visualizations of PySOMVis
Visualizations are based on the Chain Link Data set (). It is synthetic data representing two intertwined rings, which presents the topology violations after projection. The SOM map represents 18x12 neurons trained 10000 times, learnRate=0.7, sigma=7.
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-pjk6{border-color:#000000;color:#000000;text-align:left;vertical-align:top}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
</style>
<table  class="tg">
<thead>
  <tr>
    <th class="tg-pjk6"><img src="PySOMVis/pics/git/activhist.png" width=250/> Activity Histogram</th>
    <th class="tg-0pky"><img src="PySOMVis/pics/git/clustercon.png" width=250/> Cluster Connection</th>
    <th class="tg-0pky"><img src="PySOMVis/pics/git/compplane.png" width=250/> Component Plane</th>
    <th class="tg-0pky"><img src="PySOMVis/pics/git/dmatrix.png" width=250/> D-Matrix</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/graphbased.png" width=250/> Graph based</td>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/hithist.png" width=250/> Hit Histogram</td>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/metromap.png" width=250/> Metro Map</td>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/minimspantree.png" width=250/> Minimum Spanning Tree</td>
  </tr>
  <tr>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/piechart.png" width=250/> Pie Chart</td>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/qerror.png" width=250/> Quantization Error</td>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/sdh.png" width=250/> Smoothed Data Histogram</td>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/skymeth.png" width=250/> Sky Metaphor</td>
  </tr>
  <tr>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/toperror.png" width=250/> Topology Error</td>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/Umatrix.png" width=250/> U-Matrix</td>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/Ustarmatrix.png" width=250/> U*-Matrix</td>
    <td class="tg-0pky"><img src="PySOMVis/pics/git/activhist.png" width=250/> Activity Histogram</td>
  </tr>
</tbody>
</table>

 # Citation
1. Sergei Mnishko and Andreas Rauber. Som visualization framework in python, including somstreamvis, a time series visualization. In Jan Faigl, Madalina Olteanu, and Jan Drchal, editors, Advances in Self-Organizing Maps, Learning Vector Quantization, Clustering and Data Visualization, pages 98–107, Cham, 2022. Springer International Publishing. DOI: https://doi.org/10.1007/978-3-031-15444-7_10
