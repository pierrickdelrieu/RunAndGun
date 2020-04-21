import pygame
from constante import *


class Menu:
    def __init__(self,fenetre):
        self.fenetre = fenetre
        
  
    
    def barre_chargement(self):
        global continuer
        continuer = 0
        
        font = pygame.font.Font(None,100)
        nom_jeu = font.render("Projet Transverse",1,(255,255,255)) #(nom fichier, taille)
        WHITE = pygame.Color(255, 255, 255)
        COLOR = pygame.Color(59, 215, 200)
        suivi = 0
        temps_exe = 4
        
        
        while ((suivi < 200) and (continuer == 0)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = 1

            self.fenetre.blit(nom_jeu, (400, 200))
            pygame.draw.rect(self.fenetre, WHITE, (300,400,800,35))  #(abscisse,ordonné,longuer,hauteur)
            pygame.draw.rect(self.fenetre, COLOR, (300,400,suivi*temps_exe,35))  #(abscisse,ordonné,longueur,hauteur)
            suivi = suivi + 1

            pygame.display.flip()
            



    
    
