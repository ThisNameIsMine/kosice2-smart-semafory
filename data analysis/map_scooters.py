import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium

df = pd.read_csv("./kosice2-crying_in_the_library/data analysis/Waze Data 2508 Košice_fixed.csv",nrows=30000,sep=";")
#print(df.head())
#df = df.dropna(axis=0)
df_geo = df[(df.City == "Košice") & (df.Type == "ACCIDENT") & (df.Subtype == "ACCIDENT_MAJOR")]["Location"].copy()
df_geo2 = df[(df.City == "Košice") & (df.Type == "JAM")]["Location"].copy()

print(df_geo2.head())

X_arr = []
Y_arr = []
X_arr2 = []
Y_arr2 = []
for s in df_geo:
   start = s.index("(") +1
   end = s.index(")")
   finish = s[start:end]
   X,Y = finish.split(" ") 
   X_arr.append(float(X))
   Y_arr.append(float(Y))

for s in df_geo2:
   start = s.index("(") +1
   end = s.index(")")
   finish = s[start:end]
   X,Y = finish.split(" ") 
   X_arr2.append(float(X))
   Y_arr2.append(float(Y))

dfxy = pd.DataFrame(np.array(X_arr),columns=['X'])
dfxy["Y"] = np.array(Y_arr)

dfxy2 = pd.DataFrame(np.array(X_arr2),columns=['X'])
dfxy2["Y"] = np.array(Y_arr2)

obs = list(zip(dfxy['Y'], dfxy['X']))
map_osm = folium.Map(location=[dfxy['Y'].mean(), dfxy['X'].mean()], zoom_start=17)
for el in obs:
    folium.CircleMarker(el[0:2],color="red", radius=0.075).add_to(map_osm)

map_osm.save("./map_accidents.html")

obs2 = list(zip(dfxy2['Y'], dfxy2['X']))
map_osm2 = folium.Map(location=[dfxy2['Y'].mean(), dfxy2['X'].mean()], zoom_start=17)
for el in obs2:
    folium.CircleMarker(el[0:2],color="red", radius=0.075).add_to(map_osm2)

map_osm2.save("./map_jams.html")
