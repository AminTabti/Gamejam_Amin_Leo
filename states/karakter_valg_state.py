"""
Dette er staten for hovedmenyen.
"""

from states.base_state import BaseState
import pygame
from random import randint

class SelectionState(BaseState):
    def __init__(self):
        super().__init__()
        self.valgtBirk = False
        self.valgtHerman = False
        self.valgtDoomfist = False
        self.bakgrunn_load = pygame.image.load("assets/karakter_valg.png").convert()
        self.bakgrunn = pygame.transform.scale(self.bakgrunn_load, (1300, 700))
        self.start_box = pygame.Rect(80, 60, 360, 545)
        self.start_box2 = pygame.Rect(450, 60, 390, 545) #x, y, bredde, høyde
        self.start_box3 = pygame.Rect(860, 55, 375, 550)
        self.selection_player1 = False
        self.valg_player1 = None # for å lagre valg til p1

#Lyder her_____________________________________________________________________
        self.feit_latter = pygame.mixer.Sound("assets/feit_latter.wav")
        self.rap = pygame.mixer.Sound("assets/RAP.mp3")
        self.promp = pygame.mixer.Sound("assets/promp.mp3")
        self.doom_v1 = pygame.mixer.Sound("assets/doom_voice1.mp3")
        self.herman_v1 = pygame.mixer.Sound("assets/herman_voice1.mp3")
#________________________________________________________________________________

    def start_musikk(self):
        pygame.mixer.Sound("assets/click_menu.mp3").play()
        pygame.mixer.music.load("assets/Selection_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
    
    def slutt_musikk(self):
        pygame.mixer.music.fadeout(1000)

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    klikket_karakter = None
                    if self.start_box.collidepoint(event.pos):
                        klikket_karakter = "herman"
                        pygame.mixer.stop()
                        for i in range (20):
                            self.herman_v1.play()

                    elif self.start_box2.collidepoint(event.pos):
                        klikket_karakter = "doomfist"
                        pygame.mixer.stop()
                        for i in range (20):
                            self.doom_v1.play()

                    elif self.start_box3.collidepoint(event.pos):
                        klikket_karakter = "birk"
                        pygame.mixer.stop()
                        for i in range (10):
                            self.feit_latter.play()
                            self.rap.play()
                            self.promp.play()

                    if klikket_karakter:
                        if not self.selection_player1: # fant ikke en bedre måte
                            self.valg_player1 = klikket_karakter
                            self.selection_player1 = True
                        else:
                            self.persist["karakter_p1"] = self.valg_player1 #Brukte chat for å finne ut av hvordan jeg kan lagre variabeler i forskjellige filer
                            self.persist["karakter_p2"] = klikket_karakter
                            self.selection_player1 = False
                            self.next_state = "GAME"
                            self.done = True


    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakgrunn, (0,0))
        pygame.draw.rect(surface,(255,0,0), self.start_box, 2)
        pygame.draw.rect(surface,(255,0,0), self.start_box2, 2)
        pygame.draw.rect(surface,(255,0,0), self.start_box3, 2)
        if self.selection_player1 == True:
            self.draw_text(surface, "PLAYER 2", self.font, (255,0, 0), (875, 60))
        else:
            self.draw_text(surface, "PLAYER 1", self.font, (255,0, 0), (875, 60))