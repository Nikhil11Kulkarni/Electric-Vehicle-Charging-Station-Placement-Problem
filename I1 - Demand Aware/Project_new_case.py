#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import files
import osmnx as ox
import os
import networkx as nx
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
from threading import Thread
matplotlib.use('Qt5Agg')


# In[2]:


#Get the map of chandigarh
G = ox.graph_from_bbox(30.7728,30.6698,76.8202,76.6842, network_type='drive')  


# In[3]:


# projecting the graph
G_projected = ox.project_graph(G)
ox.plot_graph(G_projected)


# In[4]:


#Save the graph
ox.save_graph_shapefile(G_projected,filename='chandigarh')


# In[5]:


#loading the graph back
G = ox.load_graphml('chandigarh.graphml')
fig, ax = ox.plot_graph(G)
ax.set_title('Chandigarh Map')


# In[7]:


# get the nearest network node to each point
orig_node = ox.get_nearest_node(G, (30.72331046,76.7449385))
dest_node = ox.get_nearest_node(G, (30.70527403,76.73457478))


# In[8]:


# find the route between these nodes using dijkstra then plot it
route = nx.shortest_path(G, orig_node, dest_node, weight='length')
fig, ax = ox.plot_graph_route(G, route, node_size=0)


# In[9]:


#display the route
ax.set_title('Example route')
ax.set_ylabel('Logitude')
ax.set_xlabel('Latitude')
ax.legend(['Route'])
fig.tight_layout()
fig


# In[10]:


# display the length of the path
route = nx.shortest_path_length(G, orig_node, dest_node, weight='length')
route


# In[11]:


# how far is it between these two nodes as the crow flies?
ox.great_circle_vec(30.72331046,76.7449385,
                    30.70527403,76.73457478)


# In[12]:


#save the graph
ox.save_graphml(G, filename='Chandigarh.graphml')


# In[13]:


#load the graph
G = ox.load_graphml('Chandigarh.graphml')


# In[18]:


#read the supply and demand points
file = 'demand2.xlsx' #CHANGED: 'demand_compiled.xlsx'
demand = pd.ExcelFile(file)
print(demand.sheet_names)

df1 = demand.parse('Sheet1')
file1 = 'supply.xlsx'
supply= pd.ExcelFile(file1)
print(supply.sheet_names)
df2 = supply.parse('Sheet1')

fig = plt.figure('cube')
plt.plot(df1['Lon'], df1['Lat'], 'ro',label="Demand");
plt.plot(df2['Lon'], df2['Lat'], 'bo',label="Supply");
plt.legend(loc='upper left')
fig.suptitle('Demand points')
plt.xlabel("latitude");
plt.ylabel("longitude");


# In[13]:


df2.size/3


# In[11]:


# distance using the map is to generate the distance matrix of Demand X supply points
def Distance_using_map(df1,df2):
    time_value=0;    
    total=len(df1)
    D=np.zeros((len(df1),len(df2)), dtype=float);
    D-=1
    print(total)
    no_node=0;
    start = time.time()    
    for i in range(1,len(df1)):        
        orig_node = ox.get_nearest_node(G, (df1['Lat'][i],df1['Lon'][i]))
        temp=nx.shortest_path_length(G,orig_node, weight='length')
        for j in range(1,len(df2)):            
            dest_node = ox.get_nearest_node(G, (df2['Lat'][j],df2['Lon'][j]))
            try:
                D[i][j]=temp[dest_node];    
            except:
                D[i][j]=-1;
                print("Node not reachable"+str(no_node)+" "+str(i)+" "+str(j))
                no_node=no_node+1;                                
        print(total," ",D[i][1])
        total=total-1;
    end = time.time()
    time_value=end-start;
    return D*1000,time_value


# In[16]:


# running the distance matrix 
# Iteration_no and distance of first element
D1,time_value=Distance_using_map(df1,df2)


# In[17]:


print("total time taken= ",time_value)


# In[18]:


np.set_printoptions(threshold=np.inf)
D1


# In[19]:


# some of the points are not reachable because of disconnection in graph for that reason they are given very large value.
D1.shape[0]
M=max(max(x) for x in D1)
for i in range(0,D1.shape[0]):
    for j in range(0,D1.shape[1]):
        if (D1[i,j]<=0):
            D1[i,j]=M;
M=min(min(x) for x in D1)
M


# In[20]:


D1.size


# In[21]:


# save the Distance matrix 
np.savetxt('test007.out', D1, delimiter=',')   # X is an array


# In[17]:


#load the distance matrix
X = np.loadtxt('test.out', delimiter=',')   # X is an array
X.shape


# In[ ]:


# manhattan distance for the Distance not much used 
def Distance_manhattan(df1,df2):
    D=np.zeros((len(df1),len(df2)), dtype=float);
    for i in range(len(df1)):
        for j in range(len(df2)):
            D[i][j]=abs(df1['Lat'][i]-df2['Lat'][j])+abs(df1['Lon'][i]-df2['Lon'][j])
    return D*1000


# In[ ]:


D=Distance_manhattan(df1,df2)


# In[21]:


#shape of the X is 
X=X/1000
X.shape


# In[22]:


print("Average = ",np.average(X))
print("Max = ",np.max(X))
print("Min = ",np.min(X))

