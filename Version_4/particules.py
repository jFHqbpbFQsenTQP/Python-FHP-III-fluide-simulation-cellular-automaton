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
from flux_pression_vitesse import *
from interface_graphique import *
from video import *
from collections import deque


#Donne les coordonnées relatives des pixels d'un cercle
def points_dans_disque(rayon):
    points = []
    for x in range(-rayon, rayon + 1):
        for y in range(-rayon, rayon + 1):
            distance = math.sqrt(x**2 + y**2)
            if distance <= rayon:
                points.append((x, y))
    return (points, len(points))


#Fonction qui verifie si un point est dans la grille. Utiliser pour eviter les beugs.
def est_dans_grille(i,j) :
  return 0 <= i and i < lignes and 0 <= j and j < colonnes

def calcul_echantillon(rayon):
  points = []
  for x in range(rayon) : 
    points.append((x, 0))  
  return points

forme_et_surface = [points_dans_disque(r) for r in range(15)]
echantillons = [calcul_echantillon(r) for r in range(15)]

particules = []

#Deux tableaux qui comptent le nombres de particules crées et capturées. Utile pour faire le diagramme.
particules_crees = np.zeros(15)
particules_capturees = np.zeros(15)
particules_transmises = np.zeros(15)

#Si tu veux comprendre, fait un dessin. [horloge, vitesse]. Ici horloge en 6 temps.
deplacement_particule_i = [
  [-1, -1, -1, -1, -1, -1,   0,   1, 1, 1, 1, 1 ,1],
  [-1, -1, -1,  0,  0,  0,   0,   0, 0, 0, 1, 1, 1],
  [-1, -1,  0, -1,  0,  0,   0,   0, 0, 1, 0, 1, 1],
  [-1, -1, -1,  0, -1,  0,   0,   0, 1, 0, 1, 1, 1],
  [-1, -1, -1, -1,  0,  0,   0,   0, 0, 1, 1, 1, 1],
  [-1,  0,  0,  0,  0,  0,   0,   0, 0, 0, 0, 0, 1],]

deplacement_particule_j = [
  [-1, -1, -1, -1, -1, -1,   0,   1, 1, 1, 1, 1 ,1],
  [-1, -1, -1,  0,  0,  0,   0,   0, 0, 0, 1, 1, 1],
  [-1, -1,  0, -1,  0,  0,   0,   0, 0, 1, 0, 1, 1],
  [-1, -1, -1,  0, -1,  0,   0,   0, 1, 0, 1, 1, 1],
  [-1, -1, -1, -1,  0,  0,   0,   0, 0, 1, 1, 1, 1],
  [-1,  0,  0,  0,  0,  0,   0,   0, 0, 0, 0, 0, 1],]


#rem : convertisseur vraiment pas optimisé !!!
"""
ATTENTION : convention matricielle i,j 
a     d
  \ / 
b--0--e
  / \ 
c     f
          i  j
a = 1 -> -1 -1
b = 2 ->  0 -1 
c = 4 ->  1 -1
d = 8 -> -1  1
e = 16->  0  1
f = 32->  1  1
"""
convertisseur_i = [0] * 256
convertisseur_j = [0] * 256

convertisseur_i[a] = -1
convertisseur_i[b] = 0
convertisseur_i[c] = 1
convertisseur_i[d] = -1
convertisseur_i[e] = 0
convertisseur_i[f] = 1

convertisseur_j[a] = -1
convertisseur_j[b] = -1
convertisseur_j[c] = -1
convertisseur_j[d] = 1
convertisseur_j[e] = 1
convertisseur_j[f] = 1


class Particule:
    def __init__(self, i, j, forme, surface, rayon):
        self.rayon = rayon
        self.deja_comptee = False
        self.is_wall = False #je peux surement bcp mieux faire ici
        self.i = i
        self.j = j
        self.forme = forme #forme est tableau deui couple qui fournit l'information des pixels autours du coeur faisant partie de la particule
        self.surface = surface #surface est la surface de forme
        self.volume = 4 * rayon * rayon * rayon #4/3 de pi r cube
        self.vitesse_i = 0
        self.vitesse_j = 0
        self.normalise_vitesse_i = 0
        self.normalise_vitesse_j = 0
        self.inertie_i = deque() #la fille inertie permet de stoquer <volume> vitesse dans la memoire
        self.inertie_j = deque() #la fille inertie permet de stoquer <volume> vitesse dans la memoire
        for i in range(self.volume) :
            self.inertie_i.append(0)
            self.inertie_j.append(0)
        particules_crees[rayon - 1] = particules_crees[rayon - 1] + 1 #Le -1 est la car la tableau commence a 0 
    
    def update_vitesse(self, grille) : 
      if not self.is_wall :
        """
        ATTENTION : convetion matricielle i,j 

        a     d
          \ / 
        b--0--e
          / \ 
        c     f

                  i  j
        a = 1 -> -1 -1
        b = 2 ->  0 -1 
        c = 4 ->  1 -1
        d = 8 -> -1  1
        e = 16->  0  1
        f = 32->  1  1
        """

        """
        for k in range(self.surface) :
          (delta_i, delta_j) = self.forme[k] #Sur cette ligne, j'ai eu un bug que je n'arrive pas a reproduire
          i = delta_i + self.i
          j = delta_j + self.j
          if est_dans_grille(i, j) :
            flux_air = grille[i, j]
            di = convertisseur_i[flux_air & a] + convertisseur_i[flux_air & c] + convertisseur_i[flux_air & d] + convertisseur_i[flux_air & f]
            dj = convertisseur_j[flux_air & a] + convertisseur_j[flux_air & b] + convertisseur_j[flux_air & c] + convertisseur_j[flux_air & d] + convertisseur_j[flux_air & e] + convertisseur_j[flux_air & f]

            self.inertie_i.append(di)
            self.inertie_j.append(dj)

            self.vitesse_i = self.vitesse_i - self.inertie_i.popleft() + di
            self.vitesse_j = self.vitesse_j - self.inertie_j.popleft() + dj

            #le x2 et x3 permet d'avoir plus de nuance dans les vitesses. Car sinon j'avais ce probleme : "avec la division je prend la partie entiere inferieure => je suis trop vite a zero avec ma particule bloque"
            self.normalise_vitesse_i = round((3 * self.vitesse_i) / self.volume)
            self.normalise_vitesse_j = round((2 * self.vitesse_j) / self.volume)
          assert abs(self.normalise_vitesse_i) <= 6, "erreur particule_v_i est trop grand"
          assert abs(self.normalise_vitesse_j) <= 6, "erreur particule_v_j est trop grand"
        """
        for l in range(alpha) :
          for k in range(self.rayon) :
            (delta_i, delta_j) = echantillons[self.rayon][k]
            i = delta_i + self.i
            j = delta_j + self.j
            if est_dans_grille(i, j) :
              flux_air = grille[i, j]
              di = convertisseur_i[flux_air & a] + convertisseur_i[flux_air & c] + convertisseur_i[flux_air & d] + convertisseur_i[flux_air & f]
              dj = convertisseur_j[flux_air & a] + convertisseur_j[flux_air & b] + convertisseur_j[flux_air & c] + convertisseur_j[flux_air & d] + convertisseur_j[flux_air & e] + convertisseur_j[flux_air & f]

              self.inertie_i.append(di)
              self.inertie_j.append(dj)

              self.vitesse_i = self.vitesse_i - self.inertie_i.popleft() + di
              self.vitesse_j = self.vitesse_j - self.inertie_j.popleft() + dj

              #le x2 et x3 permet d'avoir plus de nuance dans les vitesses. Car sinon j'avais ce probleme : "avec la division je prend la partie entiere inferieure => je suis trop vite a zero avec ma particule bloque"
              self.normalise_vitesse_i = round((3 * self.vitesse_i) / self.volume)
              self.normalise_vitesse_j = round((2 * self.vitesse_j) / self.volume)
            assert abs(self.normalise_vitesse_i) <= 6, "erreur particule_v_i est trop grand"
            assert abs(self.normalise_vitesse_j) <= 6, "erreur particule_v_j est trop grand"

    def deplacement(self, horloge) :
      if not self.is_wall :
        di = deplacement_particule_i[horloge & 5][6 + int(self.normalise_vitesse_i)]
        dj = deplacement_particule_j[horloge & 5][6 + int(self.normalise_vitesse_j)]
        self.i = self.i + di
        self.j = self.j + dj

    def afficher(self, grille) : 
      if trace_active :
        grille[self.i, self.j] = grille[self.i, self.j] | t 
      if not self.is_wall : 
        for k in range(self.surface) :
          (delta_i, delta_j) = self.forme[k]
          i = delta_i + self.i  
          j = delta_j + self.j
          if est_dans_grille(i,j) :
            if (j == colonnes - 1 and not self.deja_comptee) :
              self.deja_comptee = True
              particules_transmises[self.rayon - 1] = particules_transmises[self.rayon - 1] + 1
            if (grille[i, j] & w == w) : #rem : je gère les cas de bord par une capture. Pas ideal. Notamment risque de biaisé les stats de captures
              particules_capturees[self.rayon - 1] = particules_capturees[self.rayon - 1] + 1
              for k in range(self.surface) :
                (delta_i, delta_j) = self.forme[k]
                i = delta_i + self.i
                j = delta_j + self.j
                if est_dans_grille(i,j) :
                  grille[i, j] = grille[i, j] | w
              self.is_wall = True
              break 
            else :
              grille[i, j] = grille[i, j] | p

def apparaitre_continu (rayon, horloge) : #je fais apparaitre mes particules la 11 eme colonne car rayon max est 11 donc eviter capture directe
  if horloge < nb_iterations-nb_iterations_de_purge :
    if horloge % 10  == 0 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[0]
      particules.append(Particule(i, 11, forme, surface, 1))
    if horloge % 25 == 5 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[1]
      particules.append(Particule(i, 11, forme, surface, 2))
    if horloge % 25 == 10 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[2]
      particules.append(Particule(i, 11, forme, surface, 3))
    if horloge % 75 == 15 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[3]
      particules.append(Particule(i, 11, forme, surface, 4))
    if horloge % 75 == 20 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[4]
      particules.append(Particule(i, 11, forme, surface, 5))
    if horloge + 1 % 200 == 75 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[5]
      particules.append(Particule(i, 11, forme, surface, 6))
    if horloge + 1% 200 == 125 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[6]
      particules.append(Particule(i, 11, forme, surface, 7))
    if horloge + 1% 200 == 175 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[7]
      particules.append(Particule(i, 11, forme, surface, 8))
    if horloge + 1% 300 == 250 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[8]
      particules.append(Particule(i, 11, forme, surface, 9))
    if horloge % 300 == 0 :
      i = random.randint(1, lignes - 1)
      forme, surface = forme_et_surface[9]
      particules.append(Particule(i, 11, forme, surface, 10))
