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
from particules import *

"""
Action des boutons
- b : fait apparaitre un paquet de petite particule pour teste les mouvement brownien
"""

"""
Ce passage est un copie-colle de mon premier code. C'est pour ça qu'il peut paraitre inutilement compliqué et que des méthodes ne sont pas utilie.
Mais cela m'évite de le refaire
"""


# Vérifier si deux objets se chevauchent
def chevauchement(objet1, objet2):
    distance = ((objet2.x - objet1.x) ** 2 + (objet2.y - objet1.y) ** 2) ** 0.5
    return distance < (objet1.rayon + objet2.rayon)


# Classe pour représenter une fibre (disque)
class Fibre:
    def __init__(self, x, y, rayon):
        self.x = x
        self.y = y
        self.rayon = rayon


# Créer les fibres aléatoirement
def genere_fibre() :
    fibres = []
    positions_occupees = []
    while len(fibres) < nb_fibres:
        x = random.randint(debut_filtre + rayon_fibre, fin_filtre - rayon_fibre)
        y = random.randint(rayon_fibre, lignes - rayon_fibre)
        # Vérifier si la nouvelle fibre se chevauche avec une fibre existante
        chevauche = False
        for fibre in fibres:
            if chevauchement(fibre, Fibre(x, y, rayon_fibre)):
                chevauche = True
                break
        # Si la nouvelle fibre ne se chevauche pas, l'ajouter à la liste
        if not chevauche:
            fibres.append(Fibre(x, y, rayon_fibre))
            positions_occupees.append((x, y))
    print("Les fibres sont crées")
    return positions_occupees

# Classe de bouton
class Bouton:
    def __init__(self, x, y, largeur, hauteur, couleur_normale, texte):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur_normale = couleur_normale
        self.texte = texte
        self.rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

    def afficher(self, surface):
        pygame.draw.rect(surface, self.couleur_normale, self.rect)
        font = pygame.font.Font(None, 36)
        texte = font.render(self.texte, True, BLANC)
        texte_rect = texte.get_rect(center=self.rect.center)
        surface.blit(texte, texte_rect)

    def survol(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


# Création des bouttons
b_go = Bouton(colonnes, 0, b_largeur, b_hauteur, BLEU, "Go")
b_reset = Bouton(colonnes, b_hauteur, b_largeur, b_hauteur, GREEN, "Reset")
b_alea = Bouton(colonnes , 2*b_hauteur, b_largeur, b_hauteur, RED, "Alea")
b_mur_horizon = Bouton(colonnes , 3*b_hauteur, b_largeur, b_hauteur, TURQUOISE_1, "Horizon")
#b_mur_vertical = Bouton(colonnes , 4*b_hauteur, b_largeur, b_hauteur, TURQUOISE_2, "Vertical")
b_fibre = Bouton(colonnes , 4*b_hauteur, b_largeur, b_hauteur, TURQUOISE_2, "Fibres")
b_flux = Bouton(colonnes , 5*b_hauteur, b_largeur, b_hauteur, ORANGE, "Flux")

buttons = [b_go, b_reset, b_alea, b_mur_horizon, b_fibre, b_flux]


def main_interface_graphique() :
    flux = False

    # Création de la fenêtre pygame
    pygame.init()
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Bouton Pygame")
    
    grille = initialize()

    grille_transpose = np.transpose(grille)

    # Boucle pygame qui sert a générer ma simulation
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            #Quand le bouton go est cliqué, on sort de la boucle pygame pour lancer la simulation
            if event.type == pygame.MOUSEBUTTONDOWN and b_go.survol():
                print("Bouton Go cliqué")
                en_cours = False 
            #Quand le bouton reset est cliqué, on vide la grille
            if event.type == pygame.MOUSEBUTTONDOWN and b_reset.survol():
                print("Bouton Reset cliqué")
                for x in range(1, colonnes - 1):
                    for y in range(1, lignes - 1):
                        grille_transpose[x, y] = 0
            #Quand le bouton horizontal est cliqué, on enleve les murs horizontaux ce qui rend la boite periodique
            if event.type == pygame.MOUSEBUTTONDOWN and b_mur_horizon.survol():
                print("Bouton Horizontal cliqué")
                if h_perio :
                  h_perio = False
                  for x in range(colonnes) :
                    grille_transpose[x, 0] = 0
                    grille_transpose[x, lignes -1] = 0
                else :
                  h_perio = True
                  for x in range(colonnes) :
                    grille_transpose[x, 0] = w
                    grille_transpose[x, lignes -1] = w
            """
            #Quand le bouton vertical est cliqué, on enleve les murs verticaux ce qui rend la boite periodique
            if event.type == pygame.MOUSEBUTTONDOWN and b_mur_vertical.survol():
                print("Bouton Vertical cliqué")
                if v_perio :
                  v_perio = False
                  for y in range(lignes) :
                    grille_transpose[0, y] = 0
                    grille_transpose[colonnes -1, y] = 0
                else :
                  v_perio = True
                  for y in range(lignes) :
                    grille_transpose[0, y] = w
                    grille_transpose[colonnes -1, y] = w
            """

            #Quand le bouton fibre est cliqué, on remplit aléatoirement la grille avec des fibres
            if event.type == pygame.MOUSEBUTTONDOWN and b_fibre.survol():
                #remarque : complexité atroce
                fibres = genere_fibre()
                forme, taille = points_dans_disque(rayon_fibre)
                for (x, y) in fibres :
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = w

            #Qaund le bouton aleatoire est cliqué, on remplit aléatoirement la grille après l'avoir réinitialisée
            if event.type == pygame.MOUSEBUTTONDOWN and b_alea.survol():
                print("Bouton Alea cliqué")
                grille = initialize()
                fill_random(nb_particules, grille, flux) 
                grille_transpose = np.transpose(grille)
            #Quand le bouton flux est cliqué, les particules vont en priorité dans la direction e
            if event.type == pygame.MOUSEBUTTONDOWN and b_flux.survol():
                print("Bouton Flux cliqué")
                flux = not flux
                print("flux = ", flux)
            #Qaund je clique sur mon maillage, je rajoute des particules ou des murs
            if event.type == pygame.MOUSEBUTTONDOWN :
                x, y = pygame.mouse.get_pos()
                if x < largeur - b_largeur :
                    #colorie les bons pixels (i represente x et j represente y)
                    samples = []
                    for i in range(1, colonnes-1): 
                        for j in range(1, lignes-1):
                            if (distance((i, j), (x, y)) < rayon_fibre) :
                                samples.append((i,j))
                    #Clique droit : je rajoute une impulsion de particule de fluide
                    if event.button == 1 :
                        for colonne, ligne in samples:
                            grille_transpose[colonne, ligne] = 63  #Pour les impulsion je met toutes les vitesses possibles
                    #Clique gauche : je rajoute des murs
                    if event.button == 3:
                        for colonne, ligne in samples:
                            grille_transpose[colonne, ligne] = w #Pour les impulsion je met toutes les vitesses possibles
            
            #Quand je presse p, je fais apparaitre des particules
            if event.type == pygame.KEYDOWN:
                x, y = pygame.mouse.get_pos()
                #b pour brownian motion
                if event.key == pygame.K_b:
                    if x < largeur - b_largeur :
                        #colorie les bons pixels (i represente x et j represente y)
                        samples = []
                        rayon = 20
                        for i in range(1, colonnes-1): 
                            for j in range(1, lignes-1):
                                if (distance((i, j), (x, y)) < rayon) :
                                    samples.append((i,j))
                    for colonne, ligne in samples:
                        grille_transpose[colonne, ligne] = grille_transpose[colonne, ligne] | p  #Pour les impulsion je met toutes les vitesses possibles
                        particules.append(Particule(ligne, colonne, [(0, 0)], 1)) #Transposé surement resolut en inversant x et y dans le append
                

                #Particule de rayon 1
                if event.key == pygame.K_1 :
                    forme, taille = forme_et_taille[0]
                    particules.append(Particule(y, x, forme, taille, 1)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p
                #Particule de rayon 2
                if event.key == pygame.K_2 :
                    forme, taille = forme_et_taille[1]
                    particules.append(Particule(y, x, forme, taille, 2)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p                #Particule de rayon 3
                if event.key == pygame.K_3 :
                    forme, taille = forme_et_taille[2]
                    particules.append(Particule(y, x, forme, taille, 3)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p                #Particule de rayon 4
                if event.key == pygame.K_4 :
                    forme, taille = forme_et_taille[3]
                    particules.append(Particule(y, x, forme, taille, 4)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p                #Particule de rayon 5
                if event.key == pygame.K_5 :
                    forme, taille = forme_et_taille[4]
                    particules.append(Particule(y, x, forme, taille, 5)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p                #Particule de rayon 6
                if event.key == pygame.K_6 :
                    forme, taille = forme_et_taille[5]
                    particules.append(Particule(y, x, forme, taille, 6)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p                #Particule de rayon 7
                if event.key == pygame.K_7 :
                    forme, taille = forme_et_taille[6]
                    particules.append(Particule(y, x, forme, taille, 7)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p                #Particule de rayon 8
                if event.key == pygame.K_8 :
                    forme, taille = forme_et_taille[7]
                    particules.append(Particule(y, x, forme, taille, 8)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p                #Particule de rayon 9
                if event.key == pygame.K_9 :
                    forme, taille = forme_et_taille[8]
                    particules.append(Particule(y, x, forme, taille, 9)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p                #Particule de rayon 10
                if event.key == pygame.K_0 :
                    forme, taille = forme_et_taille[9]
                    particules.append(Particule(y, x, forme, taille, 10)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p        
                if event.key == pygame.K_g :
                    forme, taille = forme_et_taille[14]
                    particules.append(Particule(y, x, forme, taille, 15)) #heuu, probleme avec taille. Je ne sais plus si c'est au carre ou au cube
                    for k in range(taille) :
                        (dx, dy) = forme[k]
                        grille_transpose[x + dx, y + dy] = grille_transpose[x + dx, y + dy] | p        

        fenetre.fill(BLANC)

        for x in range(colonnes):
            for y in range(lignes):
                if nb_particule_noeud[grille_transpose[x, y] & 63] == 1 :#Le & 63 permet de filtrer l'information et ne pas prendre en compte des variable comme wall ou alea. Seul les variables interessantes ici sont les vitesses 
                    fenetre.set_at((x, y), GRIS_1)
                if nb_particule_noeud[grille_transpose[x, y] & 63] == 2 :#Le & 63 permet de filtrer l'information et ne pas prendre en compte des variable comme wall ou alea. Seul les variables interessantes ici sont les vitesses 
                    fenetre.set_at((x, y), GRIS_2) 
                if nb_particule_noeud[grille_transpose[x, y] & 63] == 3 :#Le & 63 permet de filtrer l'information et ne pas prendre en compte des variable comme wall ou alea. Seul les variables interessantes ici sont les vitesses 
                    fenetre.set_at((x, y), GRIS_3) 
                if nb_particule_noeud[grille_transpose[x, y] & 63] == 4 :#Le & 63 permet de filtrer l'information et ne pas prendre en compte des variable comme wall ou alea. Seul les variables interessantes ici sont les vitesses 
                    fenetre.set_at((x, y), GRIS_4) 
                if nb_particule_noeud[grille_transpose[x, y] & 63] == 5 :#Le & 63 permet de filtrer l'information et ne pas prendre en compte des variable comme wall ou alea. Seul les variables interessantes ici sont les vitesses 
                    fenetre.set_at((x, y), GRIS_5) 
                if nb_particule_noeud[grille_transpose[x, y] & 63] == 6 :#Le & 63 permet de filtrer l'information et ne pas prendre en compte des variable comme wall ou alea. Seul les variables interessantes ici sont les vitesses 
                    fenetre.set_at((x, y), NOIR) 
                if grille_transpose[x, y] & w == w :
                    fenetre.set_at((x, y), RED)
                if grille_transpose[x, y] & p == p :
                    fenetre.set_at((x, y), RED)

        for button in buttons : 
            button.afficher(fenetre)
        pygame.display.flip()

    pygame.quit()
    #On sort de la fenêtre pygame, le code se lance 

    return (np.transpose(grille_transpose), flux)
