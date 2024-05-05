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
from particules import *

grille, flux = main_interface_graphique ()

#Initialisation, mais je sais plus pourquoi ca marche ???
states = [] #States vas stoquer chacunes de mes imges
pression_states = []
vitesse_states = []

grille_presison = calcul_pression(grille, resolution)
grille_vitesse = calcul_vitesse(grille, resolution)

states.append(turn_state(grille))
pression_states.append(grille_presison)
vitesse_states.append(grille_vitesse)

new_grille = update(grille)
new_grille_pression = calcul_pression(grille, resolution)
new_grille_vitesse = calcul_vitesse(grille, resolution)

states.append(turn_state(new_grille))
pression_states.append(new_grille_pression)
vitesse_states.append(new_grille_vitesse)

states.append(turn_state(new_grille)) #Heuuu bizare que cela soit en double ???
pression_states.append(new_grille_pression)
vitesse_states.append(new_grille_vitesse)

    #Cette boucle itère la simulation. Tqdm permet d'avoir une barre de chargement dans le terminal
if full_screen :
    if flux :
        for i in tqdm(range(nb_iterations)):
            if flux_continu_particule :
                apparaitre_continu(rayon_particule, i)
            new_grille = update_continue(new_grille) 
            for particule in particules :
                particule.afficher(new_grille) #je met le afficher en premier car c'est lui qui gère indice out of bound
                particule.update_vitesse(new_grille)
                particule.deplacement(i)
            states.append(turn_state(new_grille))
    else : 
        for i in tqdm(range(nb_iterations)):
            new_grille = update(new_grille)  
            for particule in particules :
                particule.afficher(new_grille) #je met le afficher en premier car c'est lui qui gère indice out of bound
                particule.update_vitesse(new_grille)
                particule.deplacement(i)
            states.append(turn_state(new_grille))
    #Genere l'animation une fois que chaque image est générée
    creer_animation_full_screen(states, save_name)
    sauvegarder_diagramme(particules_crees, particules_capturees, particules_transmises)

else :    
    if flux :
        for i in tqdm(range(nb_iterations)):
            if flux_continu_particule :
                apparaitre_continu(rayon_particule, i)
            new_grille = update_continue(new_grille) 
            new_grille_pression = calcul_pression(new_grille, resolution)
            new_grille_vitesse = calcul_vitesse(new_grille, resolution)
            for particule in particules :
                particule.afficher(new_grille) #je met le afficher en premier car c'est lui qui gère indice out of bound
                particule.update_vitesse(new_grille)
                particule.deplacement(i)
            states.append(turn_state(new_grille))
            pression_states.append(new_grille_pression)
            vitesse_states.append(new_grille_vitesse)
    else : 
        for i in tqdm(range(nb_iterations)):
            new_grille = update(new_grille)  
            new_grille_pression = calcul_pression(new_grille, resolution)
            new_grille_vitesse = calcul_vitesse(new_grille, resolution)
            for particule in particules :
                particule.afficher(new_grille) #je met le afficher en premier car c'est lui qui gère indice out of bound
                particule.update_vitesse(new_grille)
                particule.deplacement(i)
            states.append(turn_state(new_grille))
            pression_states.append(new_grille_pression)
            vitesse_states.append(new_grille_vitesse)
    #Genere l'animation une fois que chaque image est générée
    creer_animation(states, pression_states, vitesse_states, save_name)
    sauvegarder_diagramme(particules_crees, particules_capturees, particules_transmises)


sys.exit()
