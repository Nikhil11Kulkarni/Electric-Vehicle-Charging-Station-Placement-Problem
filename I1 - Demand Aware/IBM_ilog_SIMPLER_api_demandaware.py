# @ Nikhil

# import files
from docplex.mp.model import Model
import numpy as np
#import files
import osmnx as ox
import pandas as pd
import matplotlib
import math
import matplotlib.pyplot as plt
ox.config(log_console=True, use_cache=True)
matplotlib.use('Qt5Agg')
# getting the distance matrix 
Distance = np.loadtxt('test007.out', delimiter=',')   # X is an array
Distance.shape
Obj_value=[]
Opened_stations=[]
# In[47]:

for i in range(20,21): #CHECK
    Maximum=20;
    NbWarehouses = 289; #NbWarehouses is the candidate charging points
    NbStores = 803; # Nbstores is the demand points
    Stores = range(NbStores); # from zero to no of stores
    N_Warehouses = range(NbWarehouses);    
    model = Model("Simpler ---------- Charging station-Demand Aware")
    budget_charging_points = 100 # 20 CS * 5 mean
    # supply = model.binary_var_matrix(keys1=NbStores, keys2=NbWarehouses,key_format ="supply" )
    num_charging_points = model.integer_var_list(keys=NbWarehouses ) # CHECK
    model.add_constraint(model.sum(num_charging_points[ind] for ind in range(NbWarehouses)) <= budget_charging_points )
    model.add_constraint(model.sum((num_charging_points[w]>=1) for w in range(NbWarehouses)) <= Maximum)

    model.print_information()
    # constants:
    alpha = 0.5
    radius = 1149295 # CHECK
    utility = 10
    DemandJ = np.load("demand_cs.npy")
    # CHECK --
    # a_push = (utility*num_charging_points) #[ind]
    # b_push = (DemandJ) #[ind]
    # reward_d = model.sum((a_push[ind]*(a_push[ind]<=b_push[ind]) +b_push[ind]*(b_push[ind]<=a_push[ind])) for ind in range(len(num_charging_points)))
    reward_d = model.sum((utility*num_charging_points[ind]+ DemandJ[ind] )/2 for ind in range(len(num_charging_points)))
    print("\n\n----------print after:\n")
    model.print_information()


    model.add_kpi(reward_d, "Reward Demand")
    reward_c = model.sum( (Distance[s][w]<=radius) for w in N_Warehouses for s in Stores)
    model.add_kpi(reward_c, "Reward Charging")
    # finally the objective
    model.maximise(alpha*reward_d + (1-alpha)*reward_c)    
    msol=model.solve()
    solution=model.report()
    Obj_value+=[model.objective_value]
    print("num_charging_points:",num_charging_points)
    O=msol.get_values(num_charging_points);
    Opened_stations+=[O.count(1)]
   

# In[]

# supply_value= [ [ supply[s,w] for w in N_Warehouses] for s in Stores]
# Total_supply_value = [sum(supply_value[s][w]  for w in N_Warehouses) for s in Stores]

# In[57]:


print("\n\n------------")

from sys import stdout
if msol:
    stdout.write("Solution:")
    for v in num_charging_points:        
        stdout.write(" " + str(msol[v])+" "+str(v))
    stdout.write("\n")
else:
    stdout.write("Solve status: " + msol.get_solve_status() + "\n")


# In[58]:


# S=msol.get_value_dict(supply);


# In[59]:


# print( S.keys())


# In[60]:


# O=msol.get_values(Open);


# In[61]:


Opened_station=np.array(O);
Opened_station


# In[62]:


O.count(1)


# In[63]:


print(msol.solve_details)


# In[64]:


#read the demand and charging points from the excel sheet created by the 
file = 'demand2.xlsx'
demand = pd.ExcelFile(file)
print(demand.sheet_names)

df1 = demand.parse('Sheet1')
print("Demand = ",df1.size/3)
file1 = 'supply.xlsx'
supply= pd.ExcelFile(file1)
print(supply.sheet_names)
df2 = supply.parse('Sheet1')
print("Supply = ",df2.size/3)
fig = plt.figure('cube')
plt.plot(df1['Lon'], df1['Lat'], 'ro',label="Demand");
plt.plot(df2['Lon'], df2['Lat'], 'bo',label="Supply");
plt.legend(loc='upper left')
fig.suptitle('Demand points')
plt.xlabel("latitude");
plt.ylabel("longitude");


# In[71]:


Open=np.asarray(Opened_station)
Lat=df2['Lat']
Lat1=[]
Lon=df2['Lon']
Lon1=[]
for i in range(len(Open)):
    if Open[i] == 1:
        Lat1.append(Lat[i])
        Lon1.append(Lon[i])
print("The final cordinates of the selected Charging station is")
for i in range(len(Lat1)):
    print("Lat :",Lat1[i],"Lon :",Lon1[i])


# In[66]:


# final charging points
locations = []
for i in range(len(Lat1)):
    locations.append([Lat1[i],Lon1[i]])
locationlist = locations
print(len(locationlist))
locationlist[0]


# In[67]:


# Demand points
locations2 = []
for i in range(len(df2['Lat'])):
    locations2.append([df2['Lat'][i],df2['Lon'][i]])
locationlist2 = locations2
print(len(locationlist2))
locationlist2[7]


# In[68]:

#candidate charging locations
locations1 = []
for i in range(len(df1['Lat'])):
    locations1.append([df1['Lat'][i],df1['Lon'][i]])
locationlist1 = locations1
print(len(locationlist1))
locationlist1[7]
