Hello Reader,
This is a introduction to this folder,
First step of the project is to generate the dataset for the algorithm.
Since we know that the demand points and charging points are to be generated for the algorithm. 
These are generated heuristically :
1. Data is collected from openstreetmaps website.
  a) Demand points : Use the file demand.py to generate the file demand.xlsx (contains Latitude and Longitudes of the Demand points) and image demand.png.
  b) Charging Points : Use the file supply.py to generate the file supply.xlsx and image supply.png.
2 To Combine the nearby demand points we need to run the combine_close_points.py or combine_close_points.ipynb this will generate the files .
  variable combining_point is used to set the distance for combining nearby demand points.
demand_compiled.xlsx (compiled demand points) and weighted.out (Weighted file for demand points).
3 We need to generate the Distance matrix, use Project_new_case.ipynb or Project_new_case.py files. 
  Distance matrix is generated between the  Demand_Points X Supply_Points
4 To apply IBM_ILOG_CPLEX_optimizer use IBM_ilog_api.ipynb for better visualization using folium.(note: Before using IBM ILOG we need to install the full
  version of IBM).
  a) Set the value of the Distance matrix used and weighted file used in the program as saved in the Project_new_case.py. 
  b) Folium allows us in order to see the final results on map using heatmap.
5 Above steps 2-4 are repeated for differnt values of combine distances for demand points using these different values "distance vs performance.xlsx" file is created.
6 Distancevsperformance.ipynb is used in order to generate the objective vs time taken curve.

Note: Here i have created the matrices for different no of demand points as mentioned in the "distance vs performance.xlsx".(takes a long time) 
test_original.out  is the for the 0 distance for the variable 
test001.out  is for combining_point value = 0.001.
test002.out  is for combining_point value = 0.002.
etc.


Folders:
testX: test files store the distance matrix of the compiled distances at X distance which is combining_point.
