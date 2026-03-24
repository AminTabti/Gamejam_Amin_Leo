"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""

from states.base_state import BaseState
import pygame

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
        self.player1 = Player(300, 300, self, kontroller={
        "left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s}, farge=(30, 60, 200))

        self.player2 = Player(800, 300, self, kontroller={
        "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}, farge=(200, 60, 30))
    #-------Chat over--------------------------


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


    def update(self, dt: float):
        self.player1.update()
        self.player2.update()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakrund, (0,0))
        pygame.draw.rect(surface, (255, 0, 0), self.spill_bane1, 2)
        pygame.draw.rect(surface, (255, 0, 0), self.spill_bane2, 2)
        self.player1.draw(surface)
        self.player2.draw(surface)

class GameObject:
    def __init__(self, x, y, width, height, farge):
        self.rect = pygame.Rect(x, y, width, height)
        self.farge = farge
        
    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.farge, self.rect)


class Player(GameObject):
    def __init__(self, x, y, game, kontroller, farge):
        super().__init__(x, y, 50, 50, (30,60,200))
        self.speed = 9
        self.game = game
        self.kontroller = kontroller
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.farge, self.rect)

    def update(self):
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