from Terrain import Terrain
from Menu import Menu

import pygame
from constante import *
import importlib #permet de personnalisé l'import d'une librairie

theme = "minecraft"
niveau = "1" #le niveau correspond au tableau 2D de la map
tour_perso = 1
tab_terrain = importlib.import_module("terrain."+theme+".terrain"+niveau) #import tableau du terrain



#Initialisation de pygame
pygame.init()

fenetre = pygame.display.set_mode((largeur_terrain* largeur_tuiles, hauteur_terrain * hauteur_tuiles)) #initialise la fenetre

#Nommer la page
pygame.display.set_caption("Projet transverse")


#Affichage terrain
terrain = Terrain (theme, fenetre) #initialise la class Terrain
map = terrain.creation_tab_terrain(tab_terrain.modele_terrain)


clock = pygame.time.Clock()
continuer = 0

menu = Menu(fenetre)


#JEU
jeu = 0
#0 - barre de chargement
#1 - choix mode
#2 - choix theme
#3 - choix map
    
#Boucle de jeu
while (continuer == 0):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 1
                
    if(jeu==0):
        menu.barre_chargement()
        jeu=1
    else:
        terrain.rendu_terrain(map)
    
    pygame.display.flip()


    
pygame.quit
