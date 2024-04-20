# TO DO LIST

"""
### Debut vacances de l'Atousaint ###
0 - Voir comment je gere les actions de chaques boutons OK
1 - Reussir a reset OK
2 - Reussir a generer mes pixel aleatoirement OK
3 - Lier code source et pygame interface OK
4 - Voir la vague formee par la reponse a une impulsion OK 
5 - Rendre le code plus lisible OK
6 - Mieux comprendre le code source OK
7 - Reussir a faire de la superposition OK
### Fin vacances de l'Atousaint ####
# Semaine 1
rendez vous TIPE physique et Info OK
8 - Fixer wall OK
9 - Utiliser random OK
10 - Multiple initialisation OK
11 - Enregistrer impulsion en multiple initialisation OK
# Semaine 2
12.bis - Rendre les murs rouges OK
12.bis.bis - Choisir ou je mets les mur OK
12 - Mur periodique = Choisir quels mur mettre (car liste numpy periodique) OK
13 - Rajouter obstacle avex l'initialisateur pygame (besoin d'autre condition limite selon les formes ?) OK
# Semaine 3
14 - Flux continu OK
15 - Passer sur pygame plutot que sur matplot (generer les images + build_animation) OK
# Semaine 4
16 - Mesurer la pression (je passe a 1.50s) OK 
16bis - Afficher la pression (je pourrais toujours rajouter un lisssage temporel) OK 
# Semaine 5
17 - Mesurer le champs vecteur vitesse OK
17bis - Afficher les champs de vecteurs OK

Bonus : Faire un ecoulement continue OK

Essayer de mettre du random dans l'ecoulement initial pour casser les symetries OK
Reperer les problemes de transpose OK

# Semaine 6
18 - Implementer un deuxieme type de particule
# Semaine 7
19 - Mesurer mouvement brownien : la particule doit laisser une trace rouge derrière elle (ca doit pas demander bcp de boulot)
20 - Etudier les ordres de grandeurs pour pression, pv=nrt, 3/2kbt, vitesse onde dans l'air selon pression, etc

### Vacances de Noël###
Commencer le MCOT
Trouver un ou deux scientifique à qui écrire car ça fait style
Voir comment je peux integrer l'inertie et les particules plus grosse sans que cela me coute trop et en gardant la logique d'automate cellulaire

###Préparation aux oraux###
Faire la présentation pdf
"""

"""
Peut être le faire en C ???
C'est bizare, j'ai de particules qui disparaissent...
Probleme d'isotropie... essayer commen faire pour avoir une grille hexagonale...
rajouter la possibilite de superpose les particules avec un gradient de couleur
peut etre se passe de matplot lib pour juste ecrire pixel par pixel...peut etre mieux et peut etre plus naturel en C...
optimiser le code, peut etre avec operateur bitwise...
faire un mode periodique
faire un mode flux coninue
rejouter mes mesures : 
-vecteur moyen
-pression
gerer les collisions avec des surfaces arrondie
tester mon code avec experience physique
rajouter des couleurs ?
Peut être que le C me ferait gagner bcp de temps...

Euhhhh, j'ai inversé ligne et colonne dans tout mon code autre que l'initialisation... Trop galère a ratrapper...
J'ai utilise deux convention : (i,j) matrice et (x, y) classique pour ordi
(i, j) : horible a changer

J'ai un probleme avec le mouvement brownien je pense + pas assez d'inertie.
Pour le mouvement brownien, je pensais que si je diminuais la densité de particules, j'aurais un  mouvmenet encore plus cahotique. Sauf que Je reste tout les temps imobile. C'est le modèle. Why not.
Pour brownien, il faudrait que j'agrandisse legerement la zone de capture (dans l'idée, rajouté une composante "electrique")

J'ai des problemes de constantes pour l'inertie + pas assez de precision

A faire :
-rajouter precision dans deplacement Should be OK
-regler probleme odg.

"""
