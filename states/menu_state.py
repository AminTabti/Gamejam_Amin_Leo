"""
Dette er staten for hovedmenyen.
"""

from states.base_state import BaseState
import pygame
from random import randint

class MenuState(BaseState):
    def __init__(self):
        super().__init__()
        self.bakrund_load =  pygame.image.load("assets/main_menu_bilde.png").convert()
        self.bakrund = pygame.transform.scale(self.bakrund_load, (1300, 700))
        self.start_box = pygame.Rect(0, 62, 637, 343) #x, y, bredde 590, høyde
        self.bakrund = pygame.transform.scale(self.bakrund_load, (1300, 700))

    def start_musikk(self):
        a1 = randint(1,5)

        if a1 <= 2:
            pygame.mixer.music.load("assets/menu_music1.mp3")
        elif a1 <= 4:
            pygame.mixer.music.load("assets/menu_music2.mp3")
        else:
            pygame.mixer.music.load("assets/menu_music3.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    
    def slutt_musikk(self):
        pygame.mixer.music.fadeout(20)


    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                         if self.start_box.collidepoint(event.pos):
                            self.next_state = "SELECTION"
                            self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakrund, (0,0))
        #pygame.draw.rect(surface, (255, 0, 0), self.start_box, 2)
        self.draw_text(surface, "Menu", self.font, (0,0, 0), (875, 60))