import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

Noir = 0, 0, 0
Blanc = 255, 255, 255
Bleu = 0, 200, 255
Rouge = 255, 0, 0
Orange = 255, 100, 0
Vert = 0, 255, 0
Gris = 150, 150, 150
Violet = 128, 128, 128


class Bouton:

    def __init__(self, fond, couleur, texte, dx, dy, largeur, hauteur):
        
        self.fond = fond
        self.couleur = couleur
        
        self.texte = texte
        self.police = pygame.font.SysFont('freesans', 48)
        
        self.dx = dx
        self.dy = dy
        
        self.hauteur = hauteur
        self.largeur = largeur
        
        self.titre = self.police.render(self.texte, True, Noir)
        self.fond.blit(self.titre, (self.dx, self.dy))
        
        self.state = False  # enable or not

        self.rect = pygame.draw.rect(self.fond, self.couleur, (self.dx, self.dy, self.largeur, self.hauteur))
        self.fond.blit(self.titre, (self.dx, self.dy))

    def update_bouton(self, fond, action=None):
    
        self.fond = fond
        
        mouse_xy = pygame.mouse.get_pos()
        over = self.rect.collidepoint(mouse_xy)
        
        if over:
            action()
            if self.couleur == Blanc:
                self.couleur = Gris
                self.state = True
            
        self.rect = pygame.draw.rect(self.fond, self.couleur, (self.dx, self.dy, self.largeur, self.hauteur))
        self.fond.blit(self.titre, (self.dx, self.dy))

    def display_bouton(self, fond):
        self.fond = fond
        self.rect = pygame.draw.rect(self.fond, self.couleur, (self.dx, self.dy, self.largeur, self.hauteur))
        self.fond.blit(self.titre, (self.dx, self.dy))
           


class Menu:
    def __init__(self):
        self.fenetre = pygame.display.set_mode((1408, 704))
        self.boucle = True
        
        # Définition de la police
        self.police = pygame.font.SysFont('freesans', 48)

        self.creation_fond()
        self.jouer()
        self.choix_mode()
        self.choix_theme()
        self.choix_map()

    def creation_fond(self):
        self.fond = pygame.Surface(self.fenetre.get_size())
        self.fond.fill(Gris)
    
    def display_text(self, texte, couleur, font, dx, dy):
        mytext = font.render(texte, True, couleur)  # True pour antialiasing
        self.fond.blit(mytext, (dx, dy))
        
    def jouer(self):
        
        self.texte_jouer = [["NOM DU JEU", Noir, self.police, 550, 50],
                          ["JOUER", Noir, self.police, 600, 320]]
        
        self.play_bouton = Bouton(self.fond, Blanc, " ", 454, 200, 408, 300)
        self.quit_bouton  = Bouton(self.fond, Blanc, " ", 5, 5, 10, 10)

    def choix_mode(self):
        
        self.texte_mode = [["CHOIX DU MODE", Noir, self.police, 550, 50],
                           ["SOLO", Noir, self.police, 350, 350],
                           ["MULTI", Noir, self.police, 950, 350]]
        
        self.solo_bouton = Bouton(self.fond, Blanc, " ", 154, 150, 500, 500)
        self.multi_bouton = Bouton(self.fond, Blanc, " ", 754, 150, 500, 500)
        self.quit_bouton  = Bouton(self.fond, Blanc, " ", 5, 5, 10, 10)
        
    def choix_theme(self):
        
        self.texte_theme = [["CHOIX DU THEME", Noir, self.police, 550, 50],
                       ["MARIO", Noir, self.police, 100, 500],
                       ["BOB L'EPONGE", Noir, self.police, 550, 500],
                       ["STAR-WARS", Noir, self.police, 1000, 500],
                       ["MINECRAFT", Noir, self.police, 400, 250],
                       ["POKEMON", Noir, self.police, 800, 250]]
        
        self.mario_bouton = Bouton(self.fond, Rouge, " ", 54,454,400,200)
        self.bob_bouton = Bouton(self.fond, Orange, " ", 504,454,400,200)
        self.star_bouton  = Bouton(self.fond, Violet, " ", 954,454,400,200)
        self.minecraft_bouton = Bouton(self.fond, Vert, " ", 279,200,400,200)
        self.pokemon_bouton = Bouton(self.fond, Bleu, " ", 729,200,400,200)
        
    def choix_map(self):
        
        self.texte_map = [["CHOIX DU NIVEAU", Noir, self.police, 550, 50],
                       ["NIVEAU 1", Noir, self.police, 200, 200],
                       ["NIVEAU 2", Noir, self.police, 800, 200],
                       ["NIVEAU 3", Noir, self.police, 200, 500],
                       ["NIVEAU 4", Noir, self.police, 800, 500]]
        
        self.map1_bouton = Bouton(self.fond, Blanc, " ", 154,150,400,200)
        self.map2_bouton = Bouton(self.fond, Blanc, " ", 754,150,400,200)
        self.map3_bouton  = Bouton(self.fond, Blanc, " ", 154, 400,400,200)
        self.map4_bouton = Bouton(self.fond, Blanc, " ", 754,400,400,200)
        
    def boucle_jouer(self):
        while self.boucle:
            
            self.creation_fond()
            
            self.play_bouton.display_bouton(self.fond)
            self.quit_bouton.display_bouton(self.fond)
            
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    self.play_bouton.update_bouton(self.fond, action=solo)
                    self.quit_bouton.update_bouton(self.fond, action=gamequit)

            for text in self.texte_jouer:
                self.display_text(text[0], text[1], text[2], text[3], text[4])

            self.fenetre.blit(self.fond, (0, 0))
            pygame.display.update()
            clock.tick(10)

    def boucle_mode(self):
        while self.boucle:
            
            self.creation_fond()
            
            self.solo_bouton.display_bouton(self.fond)
            self.multi_bouton.display_bouton(self.fond)
            self.quit_bouton.display_bouton(self.fond)
            
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    self.solo_bouton.update_bouton(self.fond, action=solo)
                    self.multi_bouton.update_bouton(self.fond, action=multi)
                    self.quit_bouton.update_bouton(self.fond, action=gamequit)
                    
                if event.type == pygame.QUIT:
                    self.boucle = False

            for text in self.texte_mode:
                self.display_text(text[0], text[1], text[2], text[3], text[4])

            self.fenetre.blit(self.fond, (0, 0))
            pygame.display.update()
            clock.tick(10)
            
    def boucle_theme(self):
        while self.boucle:
            
            self.creation_fond()
            
            self.mario_bouton.display_bouton(self.fond)
            self.bob_bouton.display_bouton(self.fond)
            self.pokemon_bouton.display_bouton(self.fond)
            self.minecraft_bouton.display_bouton(self.fond)
            self.star_bouton.display_bouton(self.fond)
            
            self.quit_bouton.display_bouton(self.fond)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    self.mario_bouton.update_bouton(self.fond, action=mario)
                    self.bob_bouton.update_bouton(self.fond, action=bob)
                    self.pokemon_bouton.update_bouton(self.fond, action=pokemon)
                    self.minecraft_bouton.update_bouton(self.fond, action=minecraft)
                    self.star_bouton.update_bouton(self.fond, action=star)
                    self.quit_bouton.update_bouton(self.fond, action=gamequit)

            for text in self.texte_theme:
                self.display_text(text[0], text[1], text[2], text[3], text[4])

            self.fenetre.blit(self.fond, (0, 0))
            pygame.display.update()
            clock.tick(10)
            
    def boucle_map(self):
        while self.boucle:
            
            self.creation_fond()
            
            self.map1_bouton.display_bouton(self.fond)
            self.map2_bouton.display_bouton(self.fond)
            self.map3_bouton.display_bouton(self.fond)
            self.map4_bouton.display_bouton(self.fond)
            
            self.quit_bouton.display_bouton(self.fond)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    self.map1_bouton.update_bouton(self.fond, action=mario)
                    self.map2_bouton.update_bouton(self.fond, action=bob)
                    self.map3_bouton.update_bouton(self.fond, action=pokemon)
                    self.map4_bouton.update_bouton(self.fond, action=minecraft)
                    self.quit_bouton.update_bouton(self.fond, action=gamequit)

            for text in self.texte_map:
                self.display_text(text[0], text[1], text[2], text[3], text[4])

            self.fenetre.blit(self.fond, (0, 0))
            pygame.display.update()
            clock.tick(10)
            
            

def solo():
    print("Solo")

def multi():
    print("Multi")

def gamequit():
    print("Quit")
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    menu = Menu()
    #menu.boucle_jouer()
    menu.boucle_mode()
    #menu.boucle_theme()
    #menu.boucle_map()
        