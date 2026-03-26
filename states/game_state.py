"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""

from states.base_state import BaseState
from states.karakter_valg_state import SelectionState
import pygame
from random import randint
class GameState(BaseState):
    def __init__(self):
        super().__init__()
        self.bakrund_load =  pygame.image.load("assets/battlefield.png").convert()
        self.bakrund = pygame.transform.scale(self.bakrund_load, (1200, 600))
        self.spill_bane1 = pygame.Rect(225, 550, 750, 50) #x, y, bredde, høyde
        self.spill_bane2 = pygame.Rect(95, 450, 1000, 100)
       
    #----------Chat under ---------------------
    def startup(self, persistent):
        self.persist = persistent
        self.valgtBirk = self.persist.get("valgtBirk", False)
        if self.valgtBirk:
            bilde1 = "assets/Birk.png"
            self.bredde = 200
            self.høyde = 200
        else:
            self.bredde = 100
            self.høyde = 100
            bilde1 = "assets/luigi_karakter.png"
        self.player1 = Player(300, 0, self, kontroller={
        "left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s}, bilde=bilde1, hoppe_bilde="assets/Birk_hopp.png")

        self.player2 = Player(800, 0, self, kontroller={
        "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}, bilde = "assets/luigi_karakter.png", hoppe_bilde="assets/Birk_hopp.png" )
        
    #----------Chat over------------------------


    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MENU"
                    self.done = True
            
                if event.key == pygame.K_p:
                    self.next_state = "PAUSE"
                    self.done = True
    def start_musikk(self):
        pygame.mixer.music.load("assets/battlefield_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)


    def update(self, dt: float):
        self.player1.update()
        self.player2.update()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakrund, (0,0))
        #pygame.draw.rect(surface, (255, 0, 0), self.spill_bane1, 2)
        #pygame.draw.rect(surface, (255, 0, 0), self.spill_bane2, 2)
        self.player1.draw(surface)
        self.player2.draw(surface)

class GameObject:
    def __init__(self, x, y, bredde, høyde):
        self.rect = pygame.Rect(x, y, bredde, høyde)
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.rect)


class Player(GameObject):
    def __init__(self, x, y, game, kontroller, bilde):
        self.game = game
        super().__init__(x, y, self.game.bredde, self.game.høyde)
        self.speed = 9
        self.vy = 0
        self.jumping = False
        self.på_bakken = False
        
        self.kontroller = kontroller
        self.bilde = pygame.image.load(bilde)
        self.bilde = pygame.transform.scale(self.bilde, (self.game.bredde, self.game.høyde))
        
    
    def draw(self, screen):
        screen.blit(self.bilde, self.rect)

    def update(self):
        gammel_bottom = self.rect.bottom  # brukte chat for å finne ut av hvordan man gjøre at kollisjonene funker å sidene av platformene også
        
        keys = pygame.key.get_pressed()
        #---------Chat under ---------
        if keys[self.kontroller["left"]]:
            self.rect.x -= self.speed
        if keys[self.kontroller["right"]]:
            self.rect.x += self.speed
        if keys[self.kontroller["up"]] and self.på_bakken:
            self.vy = -10  
            self.på_bakken = False
        if keys[self.kontroller["down"]]:
            self.rect.y += self.speed
        #-------- Chat over ---------
        if self.jumping == True and self.på_bakken == True:
            self.vy = -8
            self.jumping = False
            if self.valgtbirk:
                self.bilde = self.hoppe_bilde
        self.vy += 0.181
        self.rect.y += self.vy         
        
        self.på_bakken = False

        if self.rect.colliderect(self.game.spill_bane1) and gammel_bottom <=self.game.spill_bane1.top :
            self.rect.bottom = self.game.spill_bane1.top
            self.vy = 0
            self.på_bakken = True
            self.bilde = self.vanlig_bilde
        if self.rect.colliderect(self.game.spill_bane2) and gammel_bottom <=self.game.spill_bane2.top  :
            self.rect.bottom = self.game.spill_bane2.top
            self.vy = 0   
            self.på_bakken = True
=======
            if self.vy <= 0:
                self.vy = 0
            else:
                self.rect.y += 5
    
        self.vy += 0.4
        self.rect.y += self.vy     
        
        self.på_bakken = False

        for platform in [self.game.spill_bane1, self.game.spill_bane2]:
            if self.rect.colliderect(platform):
                if gammel_bottom <= platform.top:
                    self.rect.bottom = platform.top
                    self.vy = 0
                    self.på_bakken = True
                    self.antall_hopp = 0

                elif self.rect.top <= platform.bottom and self.vy < 0:
                    self.rect.top = platform.bottom
                    self.vy = 0

                elif self.rect.right > platform.left and self.rect.left < platform.left:
                    self.rect.right = platform.left

                elif self.rect.left < platform.right and self.rect.right > platform.right:
                    self.rect.left = platform.right
>>>>>>> 8bbd2a159ef0ee0950333e99fbf7d97a0436bf73
