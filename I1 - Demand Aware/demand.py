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
# api call to the overpy for openstreet maps
api = overpy.Overpass()
# result contain the uniform spread of the demand points
result = api.query("""	 way['junction'='roundabout'](30.6698,76.6842,30.7728,76.8202);(._;>;);
out center;""")
size=len(result.ways)
i=0;
# result1 contain the major routes of the city demand poins
result1 = api.query("""	 (   way["name"="Madhya Marg"](30.7198,76.6842,30.7728,76.8202);(._;>;);
     way["name"="Dakshin Marg"](30.6998,76.6842,30.7728,76.8202);(._;>;);
  way["name"="Himalaya Marg"](30.6998,76.6842,30.7728,76.8202);(._;>;);
); out center;
""")
size1=len(result1.ways)

# Lat=np.zeros(size+size1);
# Lon=np.zeros(size+size1);

Lat = []
Lon = []

# Combining nearby demand points for a single result at each roundabout
for way in result.ways:
	print("Name: %s" % way.tags.get("name", "n/a"))
	print(" Highway: %s" % way.tags.get("highway", "n/a"))
	print(" Nodes:")
	Lat1=0
	Lon1=0
	c = 0
	for node in way.nodes:
		print(" Lat: %f, Lon: %f" % (node.lat, node.lon))
		Lat1+=node.lat
		Lon1+=node.lon
		c+=1
		if(c%3==0):
			Lat.append(Lat1/3)
			Lon.append(Lon1/3)
			Lat1=0
			Lon1=0
			i+=1

    # i=i+1;
# Compiling the location points
for way in result1.ways:
	print("Name: %s" % way.tags.get("name", "n/a"))
	print(" Highway: %s" % way.tags.get("highway", "n/a"))
	print(" Nodes:")
	Lat1=0
	Lon1=0
	c = 0
	for node in way.nodes:
		print(" Lat: %f, Lon: %f" % (node.lat, node.lon))
		Lat1+=node.lat
		Lon1+=node.lon
		c+=1
		if(c%3==0):
			Lat.append(Lat1/3)
			Lon.append(Lon1/3)
			Lat1 = 0
			Lon1 = 0
			i=i+1;



Lat = np.array(Lat)
Lon = np.array(Lon)

#  Plot and save the image
fig = plt.figure()
plt.plot(Lon, Lat, 'ro',label="Demand");
fig.suptitle('Demand points')
plt.legend(loc='upper left')
plt.xlabel("latitude");
plt.ylabel("longitude");
plt.show()
fig.savefig('demand.png')
#Saving the file demand points to demand.xlsx
df_demand = pd.DataFrame({'Lat':Lat,'Lon':Lon})
print(df_demand.shape)
writer = pd.ExcelWriter('demand2.xlsx', engine='xlsxwriter')
df_demand.to_excel(writer, sheet_name='Sheet1')
writer.save()

