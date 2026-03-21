"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""

from states.base_state import BaseState
import pygame

class GameState(BaseState):
    def __init__(self):
        super().__init__()
        self.bakrund_load =  pygame.image.load("Gamejam_Amin_Leo/assets/bakrundsbilde.png").convert()
        self.bakrund = pygame.transform.scale(self.bakrund_load, (1200, 600))

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
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakrund, (0,0))
        self.draw_text(surface, "Main gamet her!", self.font, (0, 0, 0), (600, 300))