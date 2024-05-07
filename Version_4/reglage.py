# Dimensions de la fenetre de simulation
colonnes = 500
lignes = 500

#Parametre de la simulation
nb_particules = 3 * 100 * 100
nb_iterations = 23
nb_iterations_de_purge = 0 #1000 pour vider le filtre pour ne pas fausser le diagramme
alpha = 40
"""
500 * 500 et 4000 iteration => 3h30 annoncé 
"""

particules_fluide_visible = False
trace_active = False

#Dimensions des bouttons
b_largeur = 100
b_hauteur = 50

#Dimensions de la fenetre pygame (je rajoute les bouttons)
largeur = colonnes + b_largeur
hauteur = max(300, lignes)

# Paramètre pour une emisssion continue de particule
flux_continu_particule = True
rayon_particule = 3

# Paramètres des fibres
rayon_fibre = 13
volume_fibre = 1 * 3.14 * rayon_fibre * rayon_fibre
epaisseur = 430 # en 0.1µm
debut_filtre = 50
fin_filtre = debut_filtre + epaisseur
#assert fin_filtre < colonnes, "filtre trop epais"
volume_total = epaisseur * lignes * 1
porosite = 0.80
nb_fibres = (volume_total - porosite*volume_total) / volume_fibre

full_screen = True
save_name = "Files/alpha_40_fibre_13.mp4"
save_name_diagramme = "Files/alpha_40_fibre_13.png"
