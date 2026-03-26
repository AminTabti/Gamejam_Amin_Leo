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
        self.bakgrunn_load =  pygame.image.load("assets/battlefield2.png").convert()
        self.bakgrunn = pygame.transform.scale(self.bakgrunn_load, (1300, 700))
        self.spill_bane2 = pygame.Rect(230, 445, 845, 85) #x, y, bredde, høyde
        self.spill_bane1 = pygame.Rect(275, 530, 775, 50) # 190, 480, 920, 20 -- ikke slett dette!
       
    def startup(self, persistent):# <-- chat, men ikke alt inni
        self.persist = persistent

        karakter_bilder = { # fikk ide fra chat å bruke ordbok
            "herman": ("assets/Herman_karakter.png", 100, 100),
            "doomfist": ("assets/Doomfist.png", 100, 100),
            "birk":  ("assets/Birk3.png", 150, 150),
            }
        
        karakter1 = persistent.get("karakter_p1", "luigi")
        karakter2 = persistent.get("karakter_p2", "luigi")

        bilde1, bredde1, høyde1 = karakter_bilder[karakter1] # chat
        bilde2, bredde2, høyde2 = karakter_bilder[karakter2] # chat

        self.player1 = Player(300, 0, self, kontroller={
        "left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s}, 
        bilde=bilde1, bredde=bredde1, høyde=høyde1, navn = ".", farge = (30, 60, 200))

        self.player2 = Player(800, 0, self, kontroller={
        "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}, 
        bilde=bilde2, bredde=bredde2, høyde=høyde2, navn = ".", farge = (255, 0, 0))
        
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
            self.player1.handle_event(event)
            self.player2.handle_event(event)


    def start_musikk(self):
        pygame.mixer.music.load("assets/battlefield_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)


    def update(self, dt: float):
        self.player1.update()
        self.player2.update()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakgrunn, (0,0))
        pygame.draw.rect(surface, (255, 0, 0), self.spill_bane1, 2)
        pygame.draw.rect(surface, (255, 0, 0), self.spill_bane2, 2)
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
    def __init__(self, x, y, game, kontroller, bilde, bredde, høyde, navn, farge):
        self.game = game
        super().__init__(x, y, bredde, høyde)
        self.navn = navn
        self.farge = farge
        self.font = pygame.font.SysFont("Times new roman", 200)

        self.speed = 7
        self.vy = 0
        self.på_bakken = False

        self.antall_hopp = 0
        self.max_hopp = 2
        
        self.kontroller = kontroller
        self.bilde = pygame.image.load(bilde)
        self.bilde = pygame.transform.scale(self.bilde, (bredde, høyde))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.kontroller["up"]:  # brukte chat for å finne ut hvordan gjøre at den ikke holdes inne
                if self.på_bakken or self.antall_hopp < self.max_hopp:
                    self.vy = -8
                    self.på_bakken = False
                    self.antall_hopp += 1

    def draw(self, screen):
        screen.blit(self.bilde, self.rect)
        tekst = self.font.render(self.navn, True, self.farge)
        screen.blit(tekst, (self.rect.centerx - tekst.get_width() // 2, self.rect.top - 185)) # chat

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[self.kontroller["left"]]: # chat
            self.rect.x -= self.speed #chat
        if keys[self.kontroller["right"]]: #chat
            self.rect.x += self.speed #chat

#-------------- chat under ----------------------------------------------
        for platform in [self.game.spill_bane1, self.game.spill_bane2]: #Horizontal sjekken
            if self.rect.colliderect(platform):
                if self.rect.centerx < platform.left:
                    self.rect.right = platform.left
                elif self.rect.centerx > platform.right:
                    self.rect.left = platform.right
# ---------------- chat over--------------------------------------------------

        if keys[self.kontroller["down"]]:
            if self.vy <= 0:
                self.vy = 0
            else:
                self.rect.y += 5
    
        self.vy += 0.225
        self.rect.y += self.vy     
        
        self.på_bakken = False

        for platform in [self.game.spill_bane1, self.game.spill_bane2]:
            if self.rect.colliderect(platform):
                if self.vy >= 0:
                    self.rect.bottom = platform.top
                    self.vy = 0
                    self.på_bakken = True
                    self.antall_hopp = 0

                elif self.vy < 0:
                    self.rect.top = platform.bottom
                    self.vy = 0