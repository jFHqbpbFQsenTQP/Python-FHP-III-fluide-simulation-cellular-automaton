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

#Permet de céer une vidéo mp4
def creer_animation(states, pression_states, vitesse_states, save_name):
    fps = 20
    nSeconds = len(states)// fps
    fig, (ax3, ax2, ax1) = plt.subplots(1, 3, figsize=(12, 5))
    
    nb_c = int(colonnes / resolution)
    nb_l = int(lignes / resolution)

    a = int(lignes/resolution)
    b = int(colonnes/resolution)
    X, Y = np.meshgrid(np.arange(b), np.arange(a-1, -1, -1)) #Ca + le -1 a la ligne 4.. : c'est du archi bidouillage

    custom_cmap = plt.cm.get_cmap('gray_r', 7) #7 nuance de gris. r pour reverse
    custom_cmap_list = [custom_cmap(i) for i in range(custom_cmap.N)] #simple copie pour pouvoir travailler dessus
    custom_cmap_list.append((1.0, 0.0, 0.0, 1.0))  #Je rajoute le rouge pour les walls 
    custom_cmap_list.append((0.0, 1.0, 0.0, 1.0))  #Je rajoute le noir pour les particules
    custom_cmap_list.append((0.0, 0.0, 0.0, 1.0))  #Je rajoute le noir pour la trace des particules
    custom_cmap = custom_cmap.from_list('custom_cmap', custom_cmap_list, 10)


    def update_image(i):
        
        #Particules
        ax1.clear()
        ax1.imshow(states[i], cmap=custom_cmap, vmin=0, vmax=9)
        ax1.set_title('Particules')
        
        #Pression
        ax2.clear()
        ax2.imshow(pression_states[i], cmap = 'viridis')
        ax2.set_title('Pression')
          
        #Vitesse
        ax3.clear()
        (u, v) = vitesse_states[i]
        norme = np.sqrt(u**2 + v**2)
        nu = u / norme
        nv = v / norme
        ax3.quiver(X, Y, nu, nv, norme, scale=20, cmap='gray_r')
        ax3.set_title('Vitesse')

    anim = FuncAnimation(fig, update_image, frames=nSeconds * fps, interval = 1000 / fps)
    anim.save(save_name, writer='ffmpeg', fps=30)

def creer_animation_full_screen(states, save_name) :
    fps = 20
    nSeconds = len(states)// fps
    fig, ax = plt.subplots()

    custom_cmap = plt.cm.get_cmap('gray_r', 7) #7 nuance de gris. r pour reverse
    custom_cmap_list = [custom_cmap(i) for i in range(custom_cmap.N)] #simple copie pour pouvoir travailler dessus
    custom_cmap_list.append((1.0, 0.0, 0.0, 1.0))  #Je rajoute le rouge pour les walls 
    custom_cmap_list.append((0.0, 1.0, 0.0, 1.0))  #Je rajoute le noir pour les particules
    custom_cmap_list.append((0.0, 0.0, 0.0, 1.0))  #Je rajoute le noir pour la trace des particules
    custom_cmap = custom_cmap.from_list('custom_cmap', custom_cmap_list, 10)

    def update_image(i):
        
        #Particules
        ax.clear()
        ax.imshow(states[i], cmap=custom_cmap, vmin=0, vmax=9)
        ax.set_title('Particules')
        
    anim = FuncAnimation(fig, update_image, frames=nSeconds * fps, interval = 1000 / fps)
    anim.save(save_name, writer='ffmpeg', fps=30)



#Rem : le diagramme bar fait n'imp, peux etre plus simple de faire ca sur exel.
def sauvegarder_diagramme(particules_crees, particules_capturees) :
    pourcentage = np.zeros(15)
    for i in range(len(particules_crees)) :
        if particules_crees[i] == 0 :
            pourcentage[i] = 100
        else :
            pourcentage[i] = 100 * particules_capturees[i] / particules_crees[i]
    plt.clf()
    # Créer le diagramme à barres
    plt.bar(range(len(pourcentage)), pourcentage, color='blue', alpha=0.7, edgecolor='black')
    #Je choisis l'echelle verticale de mon diagramme
    plt.ylim(0, 100)
    plt.xlim(0, 10) #10 car le rayon maxi est 10
    # Ajouter des étiquettes et un titre
    plt.xlabel('Taille particule')
    plt.ylabel('Pourcentage collecté')
    plt.title('Pourcentage collecté en fonction de la taille des particule')
    # Sauvegarder le graphique en tant qu'image (format PNG dans cet exemple)
    plt.savefig(save_name_diagramme)
