# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 16:44:44 2019

@author: varun
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 16:36:35 2019

@author: varun
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 23:22:00 2019

@author: varun
"""
# import files
import overpy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# api call service for the charging points 
api = overpy.Overpass()
result = api.query("""(
  //Place of workship and temple
 way['amenity'='place_of_worship']  
(30.6698,76.6842,30.7728,76.8202);
  node['amenity'='place_of_worship']  
(30.6698,76.6842,30.7728,76.8202);  
  relation['amenity'='place_of_worship'](30.6698,76.6842,30.7728,76.8202);
  //The Market place
  way['shop'='convenience']
  (30.6698,76.6842,30.7728,76.8202);
  way['amenity'='marketplace']
  (30.6698,76.6842,30.7728,76.8202);
  
  node['shop'='convenience']
  (30.6698,76.6842,30.7728,76.8202);
  node['amenity'='marketplace']
  (30.6698,76.6842,30.7728,76.8202);
  
  relation['shop'='convenience']
  (30.6698,76.6842,30.7728,76.8202);
  relation['amenity'='marketplace']
  (30.6698,76.6842,30.7728,76.8202);
  //The fuel locations:
  node['amenity'='fuel']
  (30.6698,76.6842,30.7728,76.8202);
);(._;>;);
out center;""")
size1=len(result.nodes)
size=len(result.ways)
i=0;

Lat=np.zeros(size1+size);
Lon=np.zeros(size+size1);
# compiling the points for the candidate charging locations
for way in result.ways:
    print("Name: %s" % way.tags.get("name", "n/a"))
    print(" Highway: %s" % way.tags.get("highway", "n/a"))
    print(" Nodes:")
    Lat1=0
    Lon1=0
    for node in way.nodes:
        print(" Lat: %f, Lon: %f" % (node.lat, node.lon))
        Lat1+=node.lat
        Lon1+=node.lon
    Lat[i]=Lat1/len(way.nodes)
    Lon[i]=Lon1/len(way.nodes)
    i=i+1;
for node in result.nodes:
    print("Name: %s" % node.tags.get("name", "n/a"))
    Lat[i]=node.lat
    Lon[i]=node.lon
    i=i+1;


# plot and save the figure
fig = plt.figure()
plt.plot(Lon, Lat, 'ro',label="supply");
fig.suptitle('Demand points')
plt.legend(loc='upper left')
plt.xlabel("latitude");
plt.ylabel("longitude");
fig.savefig('supply.png')
#  Writing the supply points to xlsx file
df = pd.DataFrame({'Lat':Lat,'Lon':Lon})
writer = pd.ExcelWriter('supply.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()
