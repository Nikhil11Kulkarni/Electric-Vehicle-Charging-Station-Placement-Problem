import numpy as np

num_Charging_Stations = 289
my_mean = 50
my_std = 10
demandJ = np.random.normal(loc=my_mean, scale=my_std, size=num_Charging_Stations)
budget = 100 # Total Charging Points at Charging Stations. Average = 5 (serves at rate u=10)
# maximum (ChargingStations) =  20
# print(demandJ)
# print("---->" , demandJ.mean())

for i in range(demandJ.size):
	if demandJ[i]<=0:
		demandJ[i] = -1 * demandJ[i]
		print(demandJ[i],"--Changed!")
