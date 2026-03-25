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
        self.bredde = 1200
        self.høyde  = 600
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
            self.bredde = 700
            self.høyde = 800
        else:
            self.bredde = 400
            self.høyde = 400
            bilde1 = "assets/luigi_karakter.png"
        self.player1 = Player(300, 300, self, kontroller={
        "left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s}, bilde=bilde1)

        self.player2 = Player(800, 300, self, kontroller={
        "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}, bilde = "assets/luigi_karakter.png")
        
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
        
        self.player1.draw(surface)
        self.player2.draw(surface)

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.rect)


class Player(GameObject):
    def __init__(self, x, y, game, kontroller, bilde):
        super().__init__(x, y, 50, 50)
        self.speed = 9
        self.vy = 0
        self.game = game
        self.kontroller = kontroller
        self.bilde = pygame.image.load(bilde)
        self.bilde = pygame.transform.scale(self.bilde, (self.game.bredde, self.game.høyde))
        
    
    def draw(self, screen):
        screen.blit(self.bilde, self.rect)

    def update(self):
        gammel_bottom = self.rect.bottom  # brukte chat for å finne ut av hvordan man gjøre at kollisjonene funker å sidene av platformene også
        self.vy += 0.0981
        self.rect.y += self.vy
        keys = pygame.key.get_pressed()
        #---------Chat under ---------
        if keys[self.kontroller["left"]]:
            self.rect.x -= self.speed
        if keys[self.kontroller["right"]]:
            self.rect.x += self.speed
        if keys[self.kontroller["up"]]:
            self.rect.y -= self.speed
        if keys[self.kontroller["down"]]:
            self.rect.y += self.speed
        #-------- Chat over ---------

        if self.rect.colliderect(self.game.spill_bane1) and gammel_bottom <=self.game.spill_bane1.top :
            self.rect.bottom = self.game.spill_bane1.top
            self.vy = 0
        if self.rect.colliderect(self.game.spill_bane2) and gammel_bottom <=self.game.spill_bane2.top  :
            self.rect.bottom = self.game.spill_bane2.top
            self.vy = 0   