"""
En generell spill-klasse. Dette er hovedprogrammet.
"""

import pygame
from states.base_state import BaseState
from states.menu_state import MenuState
from states.game_state import GameState
from states.pause_state import PauseState

class Spill:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Smash Bros")
        self.screen = pygame.display.set_mode((1200, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.states = {
            "MENU": MenuState(),
            "GAME": GameState(),
            "PAUSE": PauseState()
        }
        self.current_state = self.states["MENU"]
        self.current_state.start_musikk()

    def main_loop(self):
        self.handle_events()
        self.update()
        self.render()

    def handle_events(self):
        events = pygame.event.get()
        # Events håndteres i staten.
        self.current_state.handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    self.running = False

    def update(self):
        # Tiden siden forrige oppdatering. Nyttig for å gjøre frame-rate independent bevegelse.
        dt = self.clock.tick(60) / 1000.0

        # Oppdaterer staten.
        self.current_state.update(dt)

        # Sjekker om staten er ferdig. Hvis den er det, bytter vi til neste state.
        if self.current_state.done:
            next_state = self.current_state.next_state
            self.current_state.done = False
            
            if hasattr(self.current_state, "slutt_musikk"):
                self.current_state.slutt_musikk()

            if next_state:
                self.current_state = self.states[next_state]

                if hasattr(self.current_state, "start_musikk"):
                    self.current_state.start_musikk()

            else:
                self.running = False

    def render(self):
        # Tegner state
        self.current_state.draw(self.screen)
        pygame.display.flip()

while True:
    spill = Spill()
    while spill.running:
        if spill.main_loop() == "RESTART":
            break
    else:
        break

pygame.quit()