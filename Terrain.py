from constante import *
import pygame
import random

class Terrain:
    def __init__ (self, tab_terrain, theme, fenetre):
        self.tab_terrain = tab_terrain
        self.theme = theme
                
        #image terre
        image_terre1 =  pygame.transform.scale(pygame.image.load("texture/"+theme+"/terre1.png").convert_alpha(), (largeur_tuiles, hauteur_tuiles))  #charge image terre 1
        image_terre2 =  pygame.transform.scale(pygame.image.load("texture/"+theme+"/terre2.png").convert_alpha(), (largeur_tuiles, hauteur_tuiles)) #charge image terre 2
        image_terre3 =  pygame.transform.scale(pygame.image.load("texture/"+theme+"/terre3.png").convert_alpha(), (largeur_tuiles, hauteur_tuiles)) #charge image terre 3
        image_terre = [image_terre1, image_terre2, image_terre3]
        
        #image sol
        image_sol1 =  pygame.transform.scale(pygame.image.load("texture/"+theme+"/sol1.png").convert_alpha(), (largeur_tuiles, hauteur_tuiles)) #charge image sol 1
        image_sol2 =  pygame.transform.scale(pygame.image.load("texture/"+theme+"/sol2.png").convert_alpha(), (largeur_tuiles, hauteur_tuiles)) #charge image sol 2
        image_sol3 =  pygame.transform.scale(pygame.image.load("texture/"+theme+"/sol3.png").convert_alpha(), (largeur_tuiles, hauteur_tuiles)) #charge image sol 3
        
        #image vide
        image_vide = pygame.transform.scale(pygame.image.load("texture/"+theme+"/vide.png").convert_alpha(), (largeur_tuiles, hauteur_tuiles)) #charge image vide

        #image caisse
        image_caisse = pygame.transform.scale(pygame.image.load("texture/"+theme+"/caisse.png").convert_alpha(), (largeur_tuiles, hauteur_tuiles)) #charge image sol 3
        
        #image bonus
        image_bonus = [pygame.transform.scale(pygame.image.load("texture/"+theme+"/bonus.png").convert_alpha(), (largeur_tuiles, hauteur_tuiles))] #charge image bonus
        
        #definition d'un dictionnaire
        self.tuiles = {0 : image_terre1, 1 : image_terre2, 2 : image_terre3, 3 : image_sol1, 4 : image_sol2, 5 : image_sol3, 6 : image_vide, 7 : image_caisse, 8 : image_bonus}
        
        #image fond
        self.image_fond = pygame.transform.scale(pygame.image.load("texture/"+theme+"/fond.png").convert_alpha(), (largeur_terrain * largeur_tuiles, hauteur_terrain * hauteur_tuiles))
        
        #fenetre pygame
        self.fenetre = fenetre
        
        
        
    def rendu_terrain (self):
        self.fenetre.blit(self.image_fond,(0,0))
        for i in range (0, len(self.tab_terrain)):
            for j in range (0,len(self.tab_terrain[i])):
                y = i * hauteur_tuiles #unité axe des ordonnés
                x = j * largeur_tuiles #unité axe des abscisses
                self.fenetre.blit (self.tuiles.get(self.tab_terrain[i][j]), (x,y)) #blit permet d'afficher qq chose sur la fenetre
