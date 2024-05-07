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
from reglage import *



#INITIALISATION CONSTANTE

# Couleurs
BLANC = (255, 255, 255)

GRIS_5 = (42, 42, 42)
GRIS_4 = (84, 84, 84)
GRIS_3 = (126, 126, 126)
GRIS_2 = (168, 168, 168)
GRIS_1 = (210, 210, 210)

NOIR = (0, 0, 0)
BLEU = (0, 0, 255)
TURQUOISE_1 = (0, 191, 255)
TURQUOISE_2 = (64, 224, 208)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)



vitesse_possible = [1, 2, 4, 8, 16, 32]

h_perio = False
v_perio = False

resolution = 10

"""
Differente direction que je vais encoder en binaire
a     d
  \ / 
b--0--e
  / \ 
c     f
"""
#J'encode mes vecteur en binaire
a = 1
b = 2
c = 4
d = 8
e = 16
f = 32

vitesse_flux_possible = [d+e, d+f, e+f, d+e+f]
vitesse_reflux_possible = [0, b]

# w (pour wall) est une variable qui contient l'information de si il y a un mur ou non
w = 64

# r (pour random) est un variable qui prend une varaible qui prend deux valeurs alterante qui me permet de choisir une distribution quand j'ai deux choix
r = 128

# p (pour particule) est une variable qui contint l'information de si il y a un mur ou non
p = 256

#t (pour trace) est une variable qui sert juste a avoir une trace de la trajectoire de la particule
t = 512

def switch_r ():
  global r
  if r == 128 :
    r = 0
  if r == 0 :
    r = 128

#Le tableau collision prend un distribution de vitesse en binaire en un noeud et revoie la distribution de vitesse en binaire apres collision
collision = np.arange(0, 1024) #la valeur 256 est exclue

#Pas de collision, la particule continue tout droit
collision[a] = a
collision[b] = b
collision[c] = c
collision[d] = d
collision[e] = e
collision[f] = f

#Collision tête à tête
"""
1     0        
  \ / 
0--0--0 
  / \ 
0     1
"""
collision[a+f]   = b + e
collision[a+f+r] = c + d
collision[b+e]   =  a + f
collision[b+e+r] = c + d
collision[c+d]   = a + f
collision[c+d]   = b + e

#Autres collisions à deux
"""
1     0        
  \ /           
1--0--0 
  / \           
0     0

et

1     0        
  \ / 
0--0--0 
  / \
1     0

rien ne change, le particules continuent tout droit
"""

#Collision à trois
"""
1     0        
  \ / 
0--0--1 
  / \ 
1     0
"""
collision[a+c+e] = b+d+f
collision[b+d+f] = a+c+e

"""
1     0                    0     1
  \ /                        \ /
0--0--1   --collision-->   0--0--1 
  / \                        / \
0     1                    1     0
"""
collision[a+f +e] = c+d +e
collision[a+f +b] = c+d +b
collision[a+f +c] = b+e +c
collision[a+f +d] = b+e +d

collision[b+e +a] = c+d +a 
collision[b+e +f] = c+d +f
collision[b+e +c] = a+f +c
collision[b+e +d] = a+f +d

collision[c+d +a] = b+e +a 
collision[c+d +f] = b+e +f
collision[c+d +b] = a+f +b 
collision[c+d +e] = a+f +e

#Collisions a quatres du type : 
"""
1     0                    1     1       0     1
  \ /                        \ /           \ /
1--0--1   --collision-->   0--0--0  ou   1--0--1
  / \                        / \           / \ 
0     1                    1     1       1     0
"""
collision[a+f + b+e]    = a+f + c+d 
collision[a+f + b+e +r] = b+e + c+d
collision[a+f + c+d]    = a+f + b+e 
collision[a+f + c+d +r] = c+d + b+e
collision[c+d + b+e]    = c+d + a+f 
collision[c+d + b+e +r] = b+e + a+f

#Enfin toutes les autres collisions entre particules ne changent rien

#Rebond sur le mur

#cette fonction me sert à remplir le tableau collision, sans devoir le faire à la main
def rebond(direction) : 
  new_direction = 0
  if direction & a == a:
    new_direction = new_direction + f
  if direction & b == b :
    new_direction = new_direction + e
  if direction & c == c:
    new_direction = new_direction + d
  if direction & d == d:
    new_direction = new_direction + c
  if direction & e == e :
    new_direction = new_direction + b
  if direction & f == f:
    new_direction = new_direction + a
  return new_direction

for i in range(64) :
  collision[w+i] = w + rebond(i)

#Je m'occupe maintenant de l'aleatoire. Pour la lecture du code, ca aurait été plus logique de le traiter plus haut. Cependant, le traiter maintenant m'evite de rentrer plein de valeur à la main
for i in range(128) :
  collision[r + i] = collision[i]


#Cette section est une copie du code juste en haut, pour remettre les bonnes valeurs correspondant a l'aleatoire



""""""
#DEBUT de la copie
#Pas de collision, la particule continue tout droit
collision[a] = a
collision[b] = b
collision[c] = c
collision[d] = d
collision[e] = e
collision[f] = f

#Collision tête à tête
"""
1     0        
  \ / 
0--0--0 
  / \
0     1
"""
collision[a+f]   = b + e
collision[a+f+r] = c + d
collision[b+e]   =  a + f
collision[b+e+r] = c + d
collision[c+d]   = a + f
collision[c+d]   = b + e

#Autres collisions à deux
"""
1     0        
  \ /           
1--0--0 
  / \           
0     0

et

1     0        
  \ / 
0--0--0 
  / \
1     0

rien ne change, le particules continuent tout droit
"""

#Collision à trois
"""
1     0        
  \ / 
0--0--1 
  / \ 
1     0
"""
collision[a+c+e] = b+d+f
collision[b+d+f] = a+c+e

"""
1     0                    0     1
  \ /                        \ /
0--0--1   --collision-->   0--0--1 
  / \                        / \
0     1                    1     0
"""
collision[a+f +e] = c+d +e
collision[a+f +b] = c+d +b
collision[a+f +c] = b+e +c
collision[a+f +d] = b+e +d

collision[b+e +a] = c+d +a 
collision[b+e +f] = c+d +f
collision[b+e +c] = a+f +c
collision[b+e +d] = a+f +d

collision[c+d +a] = b+e +a 
collision[c+d +f] = b+e +f
collision[c+d +b] = a+f +b 
collision[c+d +e] = a+f +e

#Collisions a quatres du type : 
"""
1     0                    1     1       0     1
  \ /                        \ /           \ /
1--0--1   --collision-->   0--0--0  ou   1--0--1
  / \                        / \           / \ 
0     1                    1     1       1     0
"""
collision[a+f + b+e]    = a+f + c+d 
collision[a+f + b+e +r] = b+e + c+d
collision[a+f + c+d]    = a+f + b+e 
collision[a+f + c+d +r] = c+d + b+e
collision[c+d + b+e]    = c+d + a+f 
collision[c+d + b+e +r] = b+e + a+f
#FIN de la copie
"""
Et encore une copie comme j'ai rajoute la particule
"""
for i in range(256):
  collision[p + i] = collision[i]

"""
Et re-encore une copie pour la trace
"""

for i in range(512) :
  collision[t + i] = t | collision[i]
