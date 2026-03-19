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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = "GAME"
                    self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakrund, (0,0))
        pygame.draw.rect(surface, (255, 0, 0), self.start_box)
        self.draw_text(surface, "Du er i hovedmenyen! Trykk SPACE for å starte.", self.font, (255, 255, 255), (600, 300))