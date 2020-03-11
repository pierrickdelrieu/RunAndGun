from Terrain import Terrain
import pygame
from constante import *
import importlib #permet de personnalisé l'import d'une librairie

theme = "minecraft"
niveau = "1" #le niveau correspond au tableau 2D de la map
tour_perso = 1
tab_terrain = importlib.import_module("terrain."+theme+".terrain"+niveau)

pygame.init() #initialise pygame

fenetre = pygame.display.set_mode((largeur_terrain* largeur_tuiles, hauteur_terrain * hauteur_tuiles)) #initialise la fenetre

terrain = Terrain (tab_terrain.modele_terrain, theme, fenetre) #initialise la class Terrain
terrain.rendu_terrain() #affichage du terrain




while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        
    pygame.display.flip()
    
    
    
    
    
