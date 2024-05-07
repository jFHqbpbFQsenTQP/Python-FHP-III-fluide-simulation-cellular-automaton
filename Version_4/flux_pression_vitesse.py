import numpy as np
import matplotlib.pyplot as plt
import pylab
import random
import copy
from tqdm import tqdm
import matplotlib.animation as animation
import matplotlib as mpl
import pygame
import math
import sys
from matplotlib.animation import FuncAnimation
from initialisation_constante import *
from reglage import *


#Nombre de particule dans un noeud  
def count_set_bits(number):
    count = 0
    while number:
        count += number & 1
        number >>= 1
    return count

#Ce tableau permet d'acceder rapidement au nombre de particule dans un noeud en fonction de sa distribution de vitesse
nb_particule_noeud = np.array([count_set_bits(i) for i in range(64)])

#Ce tableau permet d'acceder rapidement a la quantité de mouvement horizontale
def calcul_vitesse_u(number):
    return (count_set_bits (number & (d + e + f)) - count_set_bits (number &(a + b + c))) #Car d,e,f selon u_x et a,b,c selon -u_x
vitesse_u = np.array([calcul_vitesse_u(i) for i in range(64)])

#Ce tableau permet d'acceder rapidement a la quantité de mouvement vertical
def calcul_vitesse_v(number):
    return (count_set_bits (number & (c+f)) - count_set_bits (number &(a+d))) #Car a,d selon u_y et c,f selon -u_y. Attention, j'ai inversé ce qui me paraissait logique car mauvais résultat.
vitesse_v = np.array([calcul_vitesse_v(i) for i in range(64)])



def distance(p1, p2):
    i = p1[0]
    j = p1[1]
    x = p2[0]
    y = p2[1]
    d = math.sqrt((i-x)**2 + (j-y)**2)
    return d

def moyenne_pression(grille, i0, j0, resolution) :
  somme = 0
  nb_valeur = resolution * resolution
  for i in range(i0, i0 + resolution):
    for j in range(j0, j0 + resolution):
      somme = somme + nb_particule_noeud[grille[i, j] & 63] #je pourrais peut être gagner un peu en efficacité en faisant directement appele à view gride sauf que les murs valent 7...
  moyenne = somme / (nb_valeur * 6) #Le *6 permet de normaliser 
  return moyenne

def calcul_pression(grille, resolution) :
    #Il faut que resolution divise colonnes et lignes
    nb_c = int(colonnes / resolution)
    nb_l = int(lignes / resolution)
    grille_pression = np.zeros((nb_l, nb_c))
    for i in range(nb_l) :
      for j in range(nb_c) :
        grille_pression[i,j] = moyenne_pression(grille, i*resolution, j*resolution, resolution)
    return grille_pression

"""
v
^
|
o --> u
"""

def moyenne_u(grille, i0, j0, resolution) :
  somme = 0
  nb_valeur = resolution * resolution
  for i in range(i0, i0 + resolution):
    for j in range(j0, j0 + resolution):
      somme = somme + vitesse_u[grille[i, j] & 63]
  moyenne = somme / (nb_valeur * 3) #On normalise en divisant par 3 car au maximum trois fleches qui pointent dans la meme direction dans un noeud
  return moyenne

def moyenne_v(grille, i0, j0, resolution) :
  somme = 0
  nb_valeur = resolution * resolution
  for i in range(i0, i0 + resolution):
    for j in range(j0, j0 + resolution):
      somme = somme + vitesse_v[grille[i, j] & 63]
  moyenne = somme / (nb_valeur * 3) #On normalise en divisant par 3 car au maximum trois fleches qui pointent dans la meme direction dans un noeud
  return -moyenne

#rem : je pourrais surement faire bcp plus efficace en passant par meshgrid
def calcul_vitesse(grille, resolution) :
    #Il faut que resolution divise colonnes et lignes
    nb_c = int(colonnes / resolution)
    nb_l = int(lignes / resolution)
    grille_u = np.zeros((nb_l, nb_c))
    grille_v = np.zeros((nb_l, nb_c))
    for i in range(nb_l) :
      for j in range(nb_c) :
        grille_u[i,j] = moyenne_u(grille, i*resolution, j*resolution, resolution)
        grille_v[i,j] = moyenne_v(grille, i*resolution, j*resolution, resolution)
    return (grille_u, grille_v)


#Fonction qui crée mon maillage vide avec des murs des 4 côtés
def initialize():
    grille = np.zeros((lignes, colonnes), dtype=int)    
    grille[0, :] = w
    grille[lignes-1, :] = w
    grille[:, 0] = w
    grille[:, colonnes-1] = w
    return grille  


#getting all possible coordinates and choosing N radnomly : definition utile pour turrrrrrf_random
i_coords, j_coords = np.meshgrid(range(lignes), range(colonnes), indexing='ij')
coordinate_grid = np.array([i_coords, j_coords])
all_coordinates = []
for i in range(1, lignes-1):
    for j in range(1, colonnes-1):
        all_coordinates.append(list(coordinate_grid[:, i, j]))
"""
a     d
  \ / 
b--0--e
  / \ 
c     f
"""
"""
#Fonction qui remplie aléatoirement mon maillage (rem : un peu barbare comme façon de faire, mais ça marche)
def fill_random(N, grille, flux) : #flux est un booleen qui me dit si toutes les particules vont dans la même direction
    nb_case = colonnes * lignes
    #Si je suis en mode flux, les particules remplissent en priorite la direction e
    if flux :
      sample_e = random.sample(all_coordinates, N % nb_case)
      N = N - (N % nb_case)
      sample_d = random.sample(all_coordinates, int(N/5))
      sample_e = random.sample(all_coordinates, int(N/5))
      sample_f = random.sample(all_coordinates, int(N/5))
      sample_a = random.sample(all_coordinates, int(N/5))
      sample_c = random.sample(all_coordinates, int(N/5) + N % 5)
      sample_b = []
    else :
      sample_a = random.sample(all_coordinates, int(N/6))
      sample_b = random.sample(all_coordinates, int(N/6))
      sample_c = random.sample(all_coordinates, int(N/6))
      sample_d = random.sample(all_coordinates, int(N/6))
      sample_e = random.sample(all_coordinates, int(N/6))
      sample_f = random.sample(all_coordinates, int(N/6) + N % 6)
    for ligne,colonne in sample_a:
        grille[ligne, colonne] = grille[ligne, colonne] + a
    for ligne,colonne in sample_b:
        grille[ligne, colonne] = grille[ligne, colonne] + b
    for ligne,colonne in sample_c:
        grille[ligne, colonne] = grille[ligne, colonne] + c 
    for ligne,colonne in sample_d:
        grille[ligne, colonne] = grille[ligne, colonne] + d 
    for ligne,colonne in sample_e:
        grille[ligne, colonne] = grille[ligne, colonne] + e 
    for ligne,colonne in sample_f:
        grille[ligne, colonne] = grille[ligne, colonne] + f 
  
    return grille
"""


def fill_random(N, grille, flux) :
  if flux :
    for i in range(lignes) :
      for j in range(colonnes) :
        grille[i,j] = grille[i,j] + random.choice(vitesse_reflux_possible) + random.choice(vitesse_flux_possible)
  else :
    sample_a = random.sample(all_coordinates, int(N/6))
    sample_b = random.sample(all_coordinates, int(N/6))
    sample_c = random.sample(all_coordinates, int(N/6))
    sample_d = random.sample(all_coordinates, int(N/6))
    sample_e = random.sample(all_coordinates, int(N/6))
    sample_f = random.sample(all_coordinates, int(N/6) + N % 6)
    for ligne,colonne in sample_a:
        grille[ligne, colonne] = grille[ligne, colonne] + a
    for ligne,colonne in sample_b:
        grille[ligne, colonne] = grille[ligne, colonne] + b
    for ligne,colonne in sample_c:
        grille[ligne, colonne] = grille[ligne, colonne] + c 
    for ligne,colonne in sample_d:
        grille[ligne, colonne] = grille[ligne, colonne] + d 
    for ligne,colonne in sample_e:
        grille[ligne, colonne] = grille[ligne, colonne] + e 
    for ligne,colonne in sample_f:
        grille[ligne, colonne] = grille[ligne, colonne] + f 

  return grille

#Fonction qui extrait du maillage un tableau qui ne contient que l'information de si ma case est occupée
#Je peux peut être supprimer cette fonction et directement ecrire dans un fichier pour faire une image ???
#??? Il faut que je regarde comment faire des vidéos a partir d'image comme on à fait dans le cours...???Peut être creer un fichier avec plein d'image ? Puis rasembler ?
def turn_state(grille):
    """
    A function to visualize the states
    """
    view_grid = np.zeros((lignes, colonnes), dtype=int)
    for i in range(lignes):
        for j in range(colonnes):
            if particules_fluide_visible :
              view_grid[i, j] = nb_particule_noeud[grille[i, j] & 63] #Le & 63 permet de filtrer l'information et ne pas prendre en compte des variable comme wall ou alea. Seul les variables interessantes ici sont les vitesses 
            if grille[i, j] & p == p : 
              view_grid[i, j] = 8
            if (grille[i, j] & t == t) and trace_active :
              view_grid[i,j] = 9
            if grille[i, j] & w == w :
              view_grid[i, j] = 7 #Whoaaa, cette etape pour gérer la couleur rouge me rajoute 0.15s par frame !!!

    return view_grid

#Fonction qui récupère les coordonnees de mes voisins (Je pourrais le stoquer comme j'y accède souvent ???)
def get_neighbors(ligne, colonne):
    neighbors = []
    neighbors.append([(ligne-1)%lignes, (colonne-1)%colonnes]) #top left
    neighbors.append([ligne, (colonne-1)%colonnes]) #left
    neighbors.append([(ligne+1)%lignes, (colonne-1)%colonnes]) #bottom left
    neighbors.append([(ligne-1)%lignes, (colonne+1)%colonnes]) # top right
    neighbors.append([ligne, (colonne+1)%colonnes]) #right
    neighbors.append([(ligne+1)%lignes, (colonne+1)%colonnes]) # bottom right
    return neighbors
"""
Remarque : l'ordre dans lequel je fais le append est important pour la fonction update.

1     4        
  \ / 
2--0--5 
  / \ 
3     6
"""

#Fonction update : c'est cette fonction qui fait tourner la simulation
def update_continue(grille):
    switch_r()
    new_grille = initialize()
    for ligne in range(lignes):
        grille[ligne, colonnes-1] = random.choice(vitesse_reflux_possible) #C'est un peu barbare, mais ca devrait marcher. Lets go ca marche ;)
    for ligne in range(lignes):
        for colonne in range(colonnes): # for each cell in the grid
            #get all of its neighbors    
            voisin = get_neighbors(ligne, colonne)
            #J'aditionne toutes les directions qui arrivent
            i0 = voisin[0][0] 
            j0 = voisin[0][1]
            i1 = voisin[1][0]
            j1 = voisin[1][1]
            i2 = voisin[2][0]
            j2 = voisin[2][1]
            i3 = voisin[3][0]
            j3 = voisin[3][1]
            i4 = voisin[4][0]
            j4 = voisin[4][1]
            i5 = voisin[5][0]
            j5 = voisin[5][1]
            #Etape laborieuse... Je peux surement mieux faire ???
            advection = (grille[i0, j0] & f) | (grille[i1, j1] & e) | (grille[i2, j2] & d) | (grille[i3, j3] & c) | (grille[i4, j4] & b) | (grille[i5, j5] & a) | (grille[ligne, colonne] & w) | r
            post_collision = collision[advection]
            new_grille[ligne, colonne] = post_collision
    for ligne in range(lignes):
        new_grille[ligne, 0] = random.choice(vitesse_flux_possible) #Laisser plus de liberte
    return new_grille


#Fonction update : c'est cette fonction qui fait tourner la simulation
def update(grille):
    switch_r()
    new_grille = initialize()
    for ligne in range(lignes):
        for colonne in range(colonnes): # for each cell in the grid
            #get all of its neighbors    
            voisin = get_neighbors(ligne, colonne)
            #J'aditionne toutes les directions qui arrivent
            i0 = voisin[0][0] 
            j0 = voisin[0][1]
            i1 = voisin[1][0]
            j1 = voisin[1][1]
            i2 = voisin[2][0]
            j2 = voisin[2][1]
            i3 = voisin[3][0]
            j3 = voisin[3][1]
            i4 = voisin[4][0]
            j4 = voisin[4][1]
            i5 = voisin[5][0]
            j5 = voisin[5][1]
            #Etape laborieuse... Je peux surement mieux faire ???
            advection = (grille[i0, j0] & f) | (grille[i1, j1] & e) | (grille[i2, j2] & d) | (grille[i3, j3] & c) | (grille[i4, j4] & b) | (grille[i5, j5] & a) | (grille[ligne, colonne] & w) | r
            post_collision = collision[advection]
            new_grille[ligne, colonne] = post_collision | (grille[ligne, colonne] & t) #le ou est pour la trace, mais je suis surpris d'en avoir besoin, je pensais que le travail avait deja été fait dans initalisation_constante.py
    return new_grille
