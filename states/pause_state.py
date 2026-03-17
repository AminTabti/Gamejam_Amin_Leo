"""
Dette er staten for hovedmenyen.
"""

from states.base_state import BaseState
import pygame

class PauseState(BaseState):
    def __init__(self):
        super().__init__()

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.next_state = "GAME"
                    self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))
        self.draw_text(surface, "game (paused) press p to continiue", 
                       pygame.font.SysFont("Algerian", 40, italic = True), (255, 255, 255), (600, 300))