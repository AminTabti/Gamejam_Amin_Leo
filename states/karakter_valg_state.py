"""
Dette er staten for hovedmenyen.
"""

from states.base_state import BaseState
import pygame
from random import randint

class SelectionState(BaseState):
    def __init__(self):
        super().__init__()
        self.bakgrunn_load2 = pygame.image.load("assets/karakter_valg.png").convert()
        self.bakgrunn2 = pygame.transform.scale(self.bakgrunn_load2, (1200, 600))
        self.start_box = pygame.Rect(80, 50, 335, 450)
        self.start_box2 = pygame.Rect(425, 50, 350, 450) #x, y, bredde, høyde
        self.start_box3 = pygame.Rect(790, 50, 325, 450)
        self.bakrund = pygame.transform.scale(self.bakgrunn_load2, (1200, 600))
        self.selection_player1 = False

        self.feit_latter = pygame.mixer.Sound("assets/feit_latter.wav")
        self.feit_latter.set_volume(1)
        self.rap = pygame.mixer.Sound("assets/RAP.mp3")
        self.rap.set_volume(1)
        self.promp = pygame.mixer.Sound("assets/promp.mp3")
        self.promp.set_volume(1) # brukte chat for å finne ut hvordan gjøre lyd høyere

    def start_musikk(self):
        pygame.mixer.Sound("assets/click_menu.mp3").play()
        pygame.mixer.music.load("assets/Selection_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
    
    def slutt_musikk(self):
        pygame.mixer.music.fadeout(1000)

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.start_box.collidepoint(event.pos):
                        if self.selection_player1 == True:
                            self.selection_player1 = False
                            self.next_state = "GAME"
                            self.done = True
                        else:
                            self.selection_player1 = True
                        
                    elif self.start_box2.collidepoint(event.pos):
                        if self.selection_player1 == True:
                            self.selection_player1 = False
                            self.next_state = "GAME"
                            self.done = True
                        else:
                            self.selection_player1 = True

                    elif self.start_box3.collidepoint(event.pos):
                        self.feit_latter.play()
                        self.rap.play()
                        self.promp.play()
                        if self.selection_player1 == True:
                            self.selection_player1 = False
                            self.next_state = "GAME"
                            self.done = True
                        else:
                            self.selection_player1 = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakgrunn2, (0,0))
        pygame.draw.rect(surface,(255,0,0), self.start_box, 2)
        pygame.draw.rect(surface,(255,0,0), self.start_box2, 2)
        pygame.draw.rect(surface,(255,0,0), self.start_box3, 2)
        if self.selection_player1 == True:
            self.draw_text(surface, "PLAYER 2", self.font, (255,0, 0), (875, 60))
        else:
            self.draw_text(surface, "PLAYER 1", self.font, (255,0, 0), (875, 60))