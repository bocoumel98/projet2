import csv
import folium
import numpy as np
import webbrowser


#implementer la class noeud
class Noeud:
    #un noeud a un nom ,des attributs sous forme de dictionnaire avec comme cle : une liste de coordonnes (latitude, longitude), la taille de la population
    #la liste des voisins sera initialisée à la creation des arcs dans le graphe
    def __init__(self, name):
        self.name = name
        self.attributs = {}
        self.listNomvoisin = []
    
    def setAttributs(self,key,values):
        self.attributs[key]=values
    def getAttributs(self,key):
        return self.attributs[key]
    def getName(self):
        return self.name
    '''Deux noeud sont egaux s'ils ont les memes noms'''
    def egale(self,noeud):
        return self.name == noeud.getName()
    #Dans le fichier transport-relationships.csv,on a la cle "cost" recuperer sa valeur la plus petite
    def getCout(self):
        return min(self.attributs['cost'])
    #recuperer le cout d'un noeud donner en parametre 
    def getCostNoeud(self,noeud):
        return self.attributs['cost'][self.listNomvoisin.index(noeud)]
#Implementer la class graphe et elle herite de tous les attributs de la class noeud et ainsi de toutes les methodes
'''
les noeuds sont representés par une liste de noeud
-Les arcs forment un dictionnaire avec comme clé les noms des noeuds et com
me valeurs une liste de noeud
'''
class Graphe(Noeud):
    def __init__(self,name):
      super().__init__(name)
      self.noeuds = []
      self.arcs = {}
    def addNoeud(self,fichiernodes):
        #On peut mettre tous les noeuds dans une liste
          #-On doit attribuer à chaque noeud ses attributs: latitude, longitude, population
          #On initialise le dictionnaire des arcs en creant la cle avec le nom noeud et la valeur avec une liste vide
        with open(fichiernodes) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                noeud = Noeud(row['id'])
                noeud.setAttributs('latitude',row['latitude'])
                noeud.setAttributs('longitude',row['longitude'])
                noeud.setAttributs('population',row['population'])
                self.noeuds.append(noeud)
                self.arcs[row['id']] = []
    def addArc(self,fichierarcs):
        #On doit ajouter les arcs dans le dictionnaire
         #- Utilisez un dictionnaire pour les arcs
         #- N'oubliez pas que le graphe est non oriente.
         #-Pour chaque noeud on mettra des tuples dans la liste de ses voisins:(noeud du voisin,cout)
         #-Gerer les exceptions
        with open(fichierarcs) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.arcs[row['src']].append((row['dst'],row['cost']))
                self.arcs[row['dst']].append((row['src'],row['cost']))
    def getNoeud(self,name):
        for noeud in self.noeuds:
            if noeud.getName()==name:
                return noeud
        return None
    def getVoisins(self,noeud):
        #Trouver les voisins d'un noeud donner en parametre et retourner une liste de noeud
        #-Utilisez la liste des voisins du noeud
        #-Utilisez la liste des arcs pour trouver les voisins
        #-Utilisez la liste des noeuds pour trouver les voisins
        liste_voisins = []
        for voisin in self.arcs[(noeud.getName())]:
            liste_voisins.append(self.getNoeud(voisin[0]))
        return liste_voisins
    def getCoordonneesVoisins(self,noeud):
        #Recuperer pour un noeud donner les latitudes et longitudes des voisins
        #Constituer des pairs de listes de coordonnees entre le point et ses voisins pour une representation sous forme de polyline
        liste_voisins = self.getVoisins(noeud)
        liste_coordonnees = []
        for voisin in liste_voisins:
            liste_coordonnees.append([noeud.getAttributs('latitude'),noeud.getAttributs('longitude')])
            liste_coordonnees.append([voisin.getAttributs('latitude'),voisin.getAttributs('longitude')])
        return liste_coordonnees
    def getListeCoordonnees(self,listeNoeuds):
       #Recuperer les coordonnees d'une liste de noeuds pour visualiser sous folium 
       #-Prend en entree une liste de nom de noeuds 
       #-Retourne une liste de sous-listes a deux elements de coordonnees
         liste_coordonnees = []
         for noeud in listeNoeuds:
                liste_coordonnees.append([noeud.getAttributs('latitude'),noeud.getAttributs('longitude')])
         return liste_coordonnees
    
    '''
     Visualiser les noeuds et les arcs sous folium   
     Entree: le parametre explored sera utilisé pour les parcours de graphe
    '''
    def visualiser(self,locationpardefaut=[52.3791890,4.899431],tiles='Stamen Toner',explored=None):
        #On initialise la carte
        m = folium.Map(location=locationpardefaut,tiles=tiles,zoom_start=12)
        #On ajoute les noeuds
        for noeud in self.noeuds:
            folium.Marker([noeud.getAttributs('latitude'),noeud.getAttributs('longitude')],popup=noeud.getName()).add_to(m)
        #On ajoute les arcs
        for noeud in self.noeuds:
            liste_coordonnees = self.getCoordonneesVoisins(noeud)
            folium.PolyLine(liste_coordonnees,color='red',weight=3,popup=noeud.getName()).add_to(m)
        #On ajoute les parcours de graphe
        for noeud in explored:
            folium.Marker([noeud.getAttributs('latitude'),noeud.getAttributs('longitude')],popup=noeud.getName(),icon=folium.Icon(color='green')).add_to(m)
        #On affiche la carte
        m.save('partie2map.html')
        #webbrowser.open('map.html')
        print('map.html')
        

G=Graphe('Amsterdam')
G.addNoeud('transport-nodes.csv')
G.addArc('transport-relationships.csv')
G.visualiser()

