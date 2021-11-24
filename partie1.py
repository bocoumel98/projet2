import pandas as pd 
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import csv
import folium
df_nodes = pd.read_csv('transport-nodes.csv')
df_relationship = pd.read_csv('transport-relationships.csv')
#afficher df_nodes   
#recuperer les villes dans dans id de df_nodes dans un tableau
i=0
ville=[]
while i<12:
    ville.append((df_nodes['id'][i]))
    i=i+1

# list pour garder  la population df_nodes dans un tableau population 
i=0
population=[]
while i<12:
    population.append((df_nodes['population'][i])/1000)
    i=i+1
#print(population)
#list pour garder les neouds et leurs destinations dans transport-relationships.csv
i=0
list_nodes=[] 
while i<15:
    list_nodes.append(((df_relationship['src'][i]),(df_relationship['dst'][i])))
    i=i+1
#construire le graphe avec df_nodes et list_nodes et le visualiser
G=nx.Graph()
G.add_nodes_from(ville)
G.add_edges_from(list_nodes)
nx.draw(G,with_labels=True,node_size=population,node_color='yellow')    
plt.show()
#ajouter les attributs longitude et latitude
def ajouterAttributs(G,dfnode,nameAttr,Index):
    node=dfnode[[Index,nameAttr]]
    nodes=node.set_index(Index).to_dict('index')
    nx.set_node_attributes(G,nodes)
ajouterAttributs(G,df_nodes,'latitude','id')
ajouterAttributs(G,df_nodes,'longitude','id')
ajouterAttributs(G,df_nodes,'population','id')
print(dict(G.nodes.data()))
#construire la carte avec les attributs longitude et latitude  et les villes    
map=folium.Map(location=[48.8566,2.3522],zoom_start=5)
def marker():
   for node in G.nodes():  
     folium.Marker(location=[G.nodes[node]['latitude'],G.nodes[node]['longitude']],popup=node,icon=folium.Icon(color='red')).add_to(map)
   map.save('map.html')
marker()

for i in G.nodes():
    folium.Marker(location=[G.nodes[i]['latitude'],G.nodes[i]['longitude']],popup=i,icon=folium.Icon(color='red')).add_to(map)
map.save('basemap.html')
'''
cette fonction permet de construire une liste de noeuds comprenant pour chaque sous-liste ses coordonnées et celles d'un voisin
ces points peuvent etres utilisés pour representer les lignes dans la carte
Input: G: graphe
Output: liste de couples representant les longitudes et latitudes d'un point et d'un ses voisins
'''
def construirePointsImage(mygraph):
    points=[]
    for i in mygraph.nodes:
        for neighbor in mygraph.neighbors(i):
            points.append(((mygraph.nodes[i]['longitude'],mygraph.nodes[i]['latitude']),(mygraph.nodes[neighbor]['longitude'],mygraph.nodes[neighbor]['latitude'])))
    return points
coordonnéesVoisins = construirePointsImage(G)
print(coordonnéesVoisins)
#Visualiser une carte du graphe avec ses noeuds et les arcs sous forme lignes
'''
A faire 
Permet de visualiser une carte du graphe avec ses noeuds et les arcs sous forme lignes
Prend en entrée:
- un graphe
- les coordonnées entre chaque point et ses voisins calculées avec la fonction ci-dessus
- Une location par defaut
- Un paramétrage de folium
Output: la carte
'''
def visualiserFolium(myGraphe,points,locationpardefaut=[52.3791890,4.899431],tiles='Stamen Toner',explored=None):
    m=folium.Map(location=locationpardefaut,zoom_start=12,tiles=tiles)
    for point in points:
        folium.PolyLine(point,color='red',weight=2.5,opacity=1).add_to(m)
    folium.Marker(location=locationpardefaut,popup='Vous etes ici',icon=folium.Icon(color='green')).add_to(m)
    if explored is not None:
        for i in explored:
            folium.Marker(location=myGraphe.nodes[i]['latitude'],popup=i,icon=folium.Icon(color='blue')).add_to(m)
    m.save('map.html')
    return m
visualiserFolium(G,coordonnéesVoisins)