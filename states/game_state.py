"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""
import os
from states.base_state import BaseState
from states.karakter_valg_state import SelectionState
import pygame
from random import randint

class GameState(BaseState):
    def __init__(self):
        super().__init__()
        self.bakgrunn_load =  pygame.image.load("assets/battlefield2.png").convert()
        self.bakgrunn = pygame.transform.scale(self.bakgrunn_load, (1300, 700))
        self.spill_bane2 = pygame.Rect(230, 445, 845, 85) #x, y, bredde, høyde
        self.spill_bane1 = pygame.Rect(275, 530, 775, 50) # 190, 480, 920, 20 -- ikke slett dette!
        
       
    def startup(self, persistent):# <-- chat, men ikke alt inni
        self.persist = persistent

        karakter_bilder = { # fikk ide fra chat å bruke ordbok
            "herman": ("assets/Herman_karakter.png", 100, 150),
            "doomfist": ("assets/Doomfist.png", 100, 150),
            "birk":  ("assets/Birk_bein.png", 150, 200),
            }
        
        karakter1 = persistent.get("karakter_p1", "luigi")
        karakter2 = persistent.get("karakter_p2", "luigi")

        bilde1, bredde1, høyde1 = karakter_bilder[karakter1] # chat
        bilde2, bredde2, høyde2 = karakter_bilder[karakter2] # chat

        self.player1 = Player(300, 200, self, kontroller={
        "left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s, "special": pygame.K_b}, 
        bilde=bilde1, bredde=bredde1, høyde=høyde1, navn = ".", farge = (30, 60, 200), karakter = karakter1)

        self.player2 = Player(800, 200, self, kontroller={
        "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN, "special": pygame.K_l}, 
        bilde=bilde2, bredde=bredde2, høyde=høyde2, navn = ".", farge = (255, 0, 0), karakter = karakter2)
        
    #----------Chat over------------------------


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
            self.player1.handle_event(event)
            self.player2.handle_event(event)


    def start_musikk(self):
        pygame.mixer.music.load("assets/battlefield_music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)


    def update(self, dt: float):
        self.player1.update()
        self.player2.update()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakgrunn, (0,0))
        pygame.draw.rect(surface, (255, 0, 0), self.spill_bane1, 2)
        pygame.draw.rect(surface, (255, 0, 0), self.spill_bane2, 2)
        self.player1.draw(surface)
        self.player2.draw(surface)

class GameObject:
    def __init__(self, x, y, bredde, høyde):
        self.rect = pygame.Rect(x, y, bredde, høyde)
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.rect)


class Player(GameObject):
    def __init__(self, x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter):
        self.game = game
        super().__init__(x, y, bredde, høyde)
        self.navn = navn
        self.farge = farge
        self.font = pygame.font.SysFont("Times new roman", 200)
        self.timer = 10000000  # fikk påmåte ideen fra chat, men brukte den på en annen måte
        self.speed = 7
        self.vy = 0
        self.på_bakken = False
        self.birk_special_bool = False
        self.birk_special_bool_ned = False
        self.special_cooldown = 0
        self.antall_hopp = 0
        self.max_hopp = 2
        
        self.kontroller = kontroller

        self.bilde = pygame.image.load(bilde)
        self.bilde = pygame.transform.scale(self.bilde, (bredde, høyde))

        self.birk_bilde = self.Load_image("Birk_bein.png",(150,200))
        self.birk_hopp = self.Load_image("Birk_hopp.png",(150,200))
        self.birk_special = self.Load_image("Birk_slam_opp.png",(150,200))
        self.birk_special_ned = self.Load_image("Birk_slam_ned.png",(200,200))
        self.promp = pygame.mixer.Sound("assets/promp.mp3")
        self.Birk_grunt = pygame.mixer.Sound("assets/Birk_hopp_lyd.wav")

        self.doom_bilde = self.Load_image("Doomfist.png",(100,150))
        self.doom_hopp = self.Load_image("doomfist_hopp.png",(100,150))

        self.herman_bilde = self.Load_image("Herman_karakter.png",(100,150))
        self.herman_hopp = self.Load_image("herman_hopp.png",(100,150))

        self.karakter = karakter
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.kontroller["up"]:  # brukte chat for å finne ut hvordan gjøre at den ikke holdes inne
                if self.på_bakken or self.antall_hopp < self.max_hopp:
                    self.vy = -8
                    self.på_bakken = False
                    self.antall_hopp += 1

    def draw(self, screen):
        screen.blit(self.bilde, self.rect)
        tekst = self.font.render(self.navn, True, self.farge)
        screen.blit(tekst, (self.rect.centerx - tekst.get_width() // 2, self.rect.top - 185)) # chat

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[self.kontroller["left"]]: # chat
            self.rect.x -= self.speed #chat
        if keys[self.kontroller["right"]]: #chat
            self.rect.x += self.speed #chat
        if keys[self.kontroller["special"]] and self.på_bakken == True and self.special_cooldown <= 0:
            self.timer = 80
            self.vy = -15
            self.birk_special_bool = True
            self.på_bakken = False
            self.special_cooldown = 390  # mellom 6 og 7 sekunder :)

        self.special_cooldown -= 1
       
        if self.timer == 1:
            self. vy = 40
            self.birk_special_bool = False
            self.birk_special_bool_ned = True


#-------------- chat under ----------------------------------------------
        for platform in [self.game.spill_bane1, self.game.spill_bane2]: #Horizontal sjekken
            if self.rect.colliderect(platform):
                if self.rect.centerx < platform.left:
                    self.rect.right = platform.left
                elif self.rect.centerx > platform.right:
                    self.rect.left = platform.right
# ---------------- chat over--------------------------------------------------

        if keys[self.kontroller["down"]]:
            if self.vy <= 0:
                self.vy = 0
            else:
                self.rect.y += 5
    
        self.vy += 0.28
        self.rect.y += self.vy

        for platform in [self.game.spill_bane1, self.game.spill_bane2]: # hjelp fra chat men skrevet selv
            if self.rect.colliderect(platform):
                if self.vy >= 0:
                    self.rect.bottom = platform.top
                    self.vy = 0
                    self.på_bakken = True
                    self.antall_hopp = 0

                elif self.vy < 0:
                    self.rect.top = platform.bottom
                    self.vy = 0
                    self.på_bakken = False
        self.timer -= 1
        
        if self.karakter == "birk":
            self.update_image_birk()
        if self.karakter == "doomfist":
            self.update_image_doomfist()
        if self.karakter == "herman":
            self.update_image_herman()

    def Load_image(self,bilde_navn,scale=None): # https://www.youtube.com/watch?v=u7XpkyemKTo for guide denne også 
        image = pygame.image.load(os.path.join("assets",bilde_navn))
        if scale is not None:
            image = pygame.transform.scale(image,scale)
        return image
    
    def update_image_birk(self):
        if self.på_bakken == False:
           self.bilde = self.birk_hopp
           self.promp.play()
           self.Birk_grunt.play()
        if self.birk_special_bool == True:
            self.bilde = self.birk_special
        if self.birk_special_bool_ned == True:
            self.bilde = self.birk_special_ned
        if self.på_bakken == True:
            self.bilde = self.birk_bilde
    
    def update_image_doomfist(self):
        if self.på_bakken == False:
           self.bilde = self.doom_hopp
        elif self.på_bakken == True:
            self.bilde = self.doom_bilde
    
    def update_image_herman(self):
        if self.på_bakken == False:
           self.bilde = self.herman_hopp
        elif self.på_bakken == True:
            self.bilde = self.herman_bilde