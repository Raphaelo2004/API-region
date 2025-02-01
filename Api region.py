#--------------------------------------------------Bibliothèques-------------------------------------------------------------------
 
#importation des biblothèques
import requests                            #communiquer avec des API et envoyer des requêtes. 
import json                                #déserealizer(transformer) le json en python
import folium                              #ajouter les pings sur la carte
import geopy                               #affiche et créer la carte
from geopy.geocoders import Nominatim      #recherche des données OSM par nom et adresse (géocodage)
import webbrowser                          #affiche automatiquement la carte du programme 

#--------------------------------------------------Programme-----------------------------------------------------------------

code=str(input("donner le code d'un département : "))                      #demander de choisir un département (str=nb entier) 
reponse=requests.get(f"https://geo.api.gouv.fr/departements/{code}")       #on récupère les informations du département


x=(json.loads(reponse.text))         #conversion du document JSON dans le dictionnaire Python.
depart=x.get('nom')                  #on obtient le nom du département par le billet d'une variable


codereg=x.get('codeRegion')                                          #on obtient le code de la Region concernée
region1=requests.get(f"https://geo.api.gouv.fr/regions/{codereg}")   #on récupère les informations de la région    
region2=json.loads(region1.text)                                     #conversion du document JSON dans le dictionnaire Python
region3=region2.get('nom')                                           #on obtient le nom de la région


region=requests.get(f"https://geo.api.gouv.fr/regions/{codereg}/departements")  #on obtient les infos des régions voisines
y=json.loads(region.text)                                                       #conversion du document JSON dans le dictionnaire Python.
list1=[]                                                                        #on créer une liste vide pour les noms des départements de la région
list2=[]                                                                        #on créer une liste vide pour les codes des départements de la région


for i in range(len(y)):          #boucle pour chaque valeurs de y
    a=y[i].get("nom")            #on obtient le nom de chaque département pour la région concernée = a
    b=y[i].get("code")           #on obtient le code de chaque département pour la région concernée = b
    list1.append(a)              #on ajoute "a" à la liste1
    list2.append(b)              #on ajoute "b" à la liste2


print(f"le departement est {depart} et son code est {code}")      #affiche le nom du département et son code
print(f"Son code région est {codereg}")                           #affiche son code région
print(f"Cette région est la/le {region3}")                        #affiche le nom de la région
print(f"\nles départements de cette région sont donc :")          #on affiche les departements et leur code ligne par ligne
for i in range(len(list1)):
    print(f"{list1[i]}-{list2[i]}")


geolocator = Nominatim(user_agent="Api region")                                             #on stock notre bibliothèque dans une variable
reglocation = geolocator.geocode(region3)                                                   #localise les coordonnées de la région
regCord = [reglocation.latitude, reglocation.longitude]                                     #on stock les coordonnées de la région choisie dans une variable
ma_carte = folium.Map(regCord, zoom_start = 8)                                              #on demarre l'affichage de la carte à une distance de 8
folium.Marker(regCord, popup = region3, icon = folium.Icon(color="red")).add_to(ma_carte)   #on place avec un ping rouge la region sur la carte


for i in range(len(list1)):                                                                        #on créer un boucle qui s'effectue pour chaque département 
    location = geolocator.geocode(list1[i])                                                        #localise les coordonnées des départements
    Cord = [location.latitude, location.longitude]                                                 #on stock les coordonnées des départements dans une variable
    folium.Marker(Cord , popup = list1[i] , icon = folium.Icon(color="blue")).add_to(ma_carte)     #on place avec un ping blue la region sur la carte
    if list1[i]==depart:                                                                           #si le département est égal au département choisi 
        folium.Marker(Cord , popup = list1[i] ,icon = folium.Icon(color="green")).add_to(ma_carte) #alors on met le département choisi en vert
    

#--------------------------------------------------Fonctions--------------------------------------------------------------------
#on exécute les fonctions
ma_carte.save("macarte.html")                      #on enregistre la carte sous un dossier html
webbrowser.open('macarte.html')                    #dès que le programme est exécuté, on ouvre la carte dans un navigateur