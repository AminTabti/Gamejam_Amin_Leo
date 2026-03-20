"""
Dette er staten for hovedmenyen.
"""

from states.base_state import BaseState
import pygame

class MenuState(BaseState):
    def __init__(self):
        super().__init__()
        self.bakrund_load =  pygame.image.load("Gamejam_Amin_Leo/assets/main_menu_bilde.png").convert()
        self.bakrund = pygame.transform.scale(self.bakrund_load, (1200, 600))
        self.start_box = pygame.Rect(0, 50, 590, 300) #x, y, bredde 590, høyde

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                         if self.start_box.collidepoint(event.pos):
                            self.next_state = "GAME"
                            self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakrund, (0,0))
        self.draw_text(surface, "Menu", self.font, (0,0, 0), (875, 60))