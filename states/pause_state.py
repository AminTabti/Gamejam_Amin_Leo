"""
Dette er staten for hovedmenyen.

denne staten funker som en restart til game state.
"""

from states.base_state import BaseState
import pygame

class PauseState(BaseState):
    def __init__(self):
        super().__init__()
        self.bakrund_load =  pygame.image.load("assets/bilder/Pause_bakrund.png").convert()
        self.bakrund = pygame.transform.scale(self.bakrund_load, (1300, 700))

    def start_musikk(self):
        pygame.mixer.music.load("assets/lyder/elevator_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
    
    def slutt_musikk(self):
        pygame.mixer.music.stop()

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.next_state = "GAME"
                    self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakrund, (0,0))
        self.draw_text(surface, "Chill lounge her, bare for chill folk", 
                       pygame.font.SysFont("Algerian", 40, italic = True), (255, 255, 255), (600, 300))