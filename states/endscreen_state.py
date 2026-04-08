"""
Dette er staten for hovedmenyen.
"""

from states.base_state import BaseState
import pygame

class EndState(BaseState):
    def __init__(self):
        super().__init__()

    def startup(self, persistent):
        self.persist = persistent

        vinner_bilder = {
            "herman": ("assets/bilder/herman_vinner.png"),
            "doomfist": ("assets/bilder/doomfist_vinner.png"),
            "birk":  ("assets/bilder/birk_vinner.png"),
            }
        
        vinner = persistent.get("vinner", "birk")
        self.vinner_navn = vinner
        self.bakrund_load = pygame.image.load(vinner_bilder[vinner]).convert() #chat ga ideen for: [vinner]
        self.bakrund = pygame.transform.scale(self.bakrund_load, (1300, 700))
        

    def start_musikk(self):
        pygame.mixer.music.load("assets/lyder/Birk_theme.mp3")
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

                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MENU"
                    self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakrund, (0,0))
        #self.draw_text(surface, self.vinner_navn, 
                       #pygame.font.SysFont("Algerian", 40, italic = True), (255, 255, 255), (600, 300))