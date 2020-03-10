from Terrain import Terrain
import pygame
from constante import *
import importlib #permet de personnalisé l'import d'une librairie

theme = "minecraft"
niveau = "1"
tour_perso = 1
tab_terrain = importlib.import_module("terrain."+theme+".terrain"+niveau)

pygame.init()

fenetre = pygame.display.set_mode((largeur_terrain* largeur_tuiles, hauteur_terrain * hauteur_tuiles))

terrain = Terrain (tab_terrain.modele_terrain, theme, fenetre)
terrain.rendu_terrain()




while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        
    pygame.display.flip()
    
    
    
    
    
