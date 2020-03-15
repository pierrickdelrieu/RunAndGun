from Terrain import Terrain

import pygame
from constante import *
import importlib #permet de personnalisé l'import d'une librairie

theme = "minecraft"
niveau = "1" #le niveau correspond au tableau 2D de la map
tour_perso = 1
tab_terrain = importlib.import_module("terrain."+theme+".terrain"+niveau) #import tableau du terrain

creation_random_terrain = importlib.import_module("terrain.creation_tab_terrain") #creer un tableau aléatoire

map = creation_random_terrain.creation_tab_terrain(tab_terrain.modele_terrain)

#Initialisation de pygame
pygame.init()
fenetre = pygame.display.set_mode((largeur_terrain* largeur_tuiles, hauteur_terrain * hauteur_tuiles)) #initialise la fenetre

#Nommer la page
pygame.display.set_caption("Projet transverse")



#Barre de chargement

WHITE = pygame.Color(255, 255, 255)
COLOR = pygame.Color(59, 215, 200)
#Affichage terrain
terrain = Terrain (map, theme, fenetre) #initialise la class Terrain


font=pygame.font.Font(None, 100) #dessiner du texte sur une nouvelle surface (..., police)
nom_jeu = font.render("Projet Transverse",1,(255,255,255)) #(nom fichier, taille)
#demarer_jeu = font.render("Cliquer pour demarer le jeu",1,(255,255,255)) #(nom fichier, taille)

continuer = 0
suivi_menu = 1
while (continuer == 0):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 1
            
    #Barre de chargement
    if((suivi_menu < 800/4) and (suivi_menu != 0)):
        fenetre.blit(nom_jeu, (400, 200))
        pygame.draw.rect(fenetre, WHITE, (300,400,800,35))  #(abscisse,ordonné,longuer,hauteur)
        pygame.draw.rect(fenetre, COLOR, (300,400,suivi_menu*4,35))  #(abscisse,ordonné,longueur,hauteur)
        suivi_menu = suivi_menu + 1
#
##    elif(suivi_menu !=0):
##        fenetre.blit(demarer_jeu, (400, 200))
##        for event in pygame.event.get():
##            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] < 100):
##                suivi_menu = 0
#
    else:
        terrain.rendu_terrain() #affichage du terrain


    
    pygame.display.flip()
    
pygame.quit
    
    
    
    
    
