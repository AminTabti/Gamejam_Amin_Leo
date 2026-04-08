"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""
import os
from states.base_state import BaseState
import pygame

class GameState(BaseState):
    def __init__(self):
        super().__init__()
        self.bakgrunn_load =  pygame.image.load("assets/bilder/battlefield2.png").convert()
        self.bakgrunn = pygame.transform.scale(self.bakgrunn_load, (1300, 700))
        self.spill_bane2 = pygame.Rect(230, 445, 845, 85) #x, y, bredde, høyde
        self.spill_bane1 = pygame.Rect(275, 530, 775, 50) # 190, 480, 920, 20 -- ikke slett dette!
        
       
    def startup(self, persistent):# <-- chat, men ikke alt inni
        self.persist = persistent

        karakter_bilder = { # fikk ide fra chat å bruke ordbok
            "herman": ("assets/bilder/Herman_karakter.png", 100, 150),
            "doomfist": ("assets/bilder/Doomfist.png", 100, 150),
            "birk":  ("assets/bilder/Birk_bein.png", 150, 200),
            }
        
        karakter1 = persistent.get("karakter_p1", "birk")
        karakter2 = persistent.get("karakter_p2", "birk")

        bilde1, bredde1, høyde1 = karakter_bilder[karakter1] # chat
        bilde2, bredde2, høyde2 = karakter_bilder[karakter2] # chat

        self.hp_bar_font = pygame.font.SysFont("Times new roman", 80, bold = True)

#------------ Hovedsakelig chat-----------------------------------------------
        self.player1 = self.lag_spiller( karakter1, 300, 200, self, { 
            "left": pygame.K_a, 
            "right": pygame.K_d,
            "up": pygame.K_w, 
            "down": pygame.K_s, 
            "special": pygame.K_c, 
            "attack": pygame.K_v, 
            "Dodge": pygame.K_LSHIFT},
            bilde1, bredde1, høyde1, "P1", (32,63,200), karakter1)
 
        self.player2 = self.lag_spiller(karakter2, 800, 200, self, {
            "left": pygame.K_LEFT, 
            "right": pygame.K_RIGHT,
            "up": pygame.K_UP, 
            "down": pygame.K_DOWN, 
            "special": pygame.K_k, 
            "attack": pygame.K_l, 
            "Dodge": pygame.K_RCTRL},
            bilde2, bredde2, høyde2, "P2", (255,0,0), karakter2)



    def lag_spiller(self, karakter, x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter_id):
        if karakter == "birk":
            return Birk(x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter_id)
        elif karakter == "doomfist":
            return Doomfist(x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter_id)
        elif karakter == "herman":
            return Herman(x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter_id)
    #----------Hovedsakelig Chat -----------------------------------

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
        pygame.mixer.music.load("assets/lyder/battlefield_music.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        


    def update(self, dt: float):
        self.player1.update()
        self.player2.update()
        
        # Melee attack
        if self.player1.melee_rect and self.player1.melee_rect.colliderect(self.player2.rect) and self.player1.melee_traff == False and self.player2.invincibility == False:
            if self.player1.karakter == "birk":
                self.player2.hp += 8
            else:
                self.player2.hp += 4
            self.player2.knockback(self.player1.attack_retning, self.player2.hp)
            self.player1.melee_traff = True

        if self.player2.melee_rect and self.player2.melee_rect.colliderect(self.player1.rect) and self.player2.melee_traff == False and self.player1.invincibility == False:
            if self.player2.karakter == "birk":
                self.player1.hp += 8
            else:
                self.player1.hp += 4
            self.player1.knockback(self.player2.attack_retning, self.player1.hp)
            self.player2.melee_traff = True

        # Special attack (Birk og doom)
        if (self.player1.birk_special_bool_ned or self.player1.doom_special_bool) and self.player1.special_traff == False and self.player2.invincibility == False:
            if self.player1.rect.colliderect(self.player2.rect):
                self.player2.hp += 14
                self.player2.knockback(self.player1.attack_retning, self.player2.hp)
                self.player1.special_traff = True

        if (self.player2.birk_special_bool_ned or self.player2.doom_special_bool) and self.player2.special_traff == False and self.player1.invincibility == False:
            if self.player2.rect.colliderect(self.player1.rect):
                self.player1.hp += 14
                self.player1.knockback(self.player2.attack_retning, self.player1.hp)
                self.player2.special_traff = True

        # Special attack (Herman)
        if self.player1.prosjektil_rect and self.player1.special_traff == False and self.player2.invincibility == False:
            if self.player1.prosjektil_rect.colliderect(self.player2.rect):
                self.player2.hp += 5
                self.player2.knockback(self.player1.attack_retning, self.player2.hp)
                self.player1.special_traff = True
        if self.player2.prosjektil_rect and self.player2.special_traff == False and self.player1.invincibility == False:
            if self.player2.prosjektil_rect.colliderect(self.player1.rect):
                self.player1.hp += 5
                self.player1.knockback(self.player2.attack_retning, self.player1.hp)
                self.player2.special_traff = True


    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakgrunn, (0,0))
        #pygame.draw.rect(surface, (255, 0, 0), self.spill_bane1, 2) # tegner spill bane hitboksen
        #pygame.draw.rect(surface, (255, 0, 0), self.spill_bane2, 2)

        #tegner karakterene
        self.player1.draw(surface)
        self.player2.draw(surface)

        #tegner HP bar
        p1_tekst = self.hp_bar_font.render(f"{int(self.player1.hp)}%", True, self.player1.farge)
        surface.blit(p1_tekst, (100, 600))
        p2_tekst = self.hp_bar_font.render(f"{int(self.player2.hp)}%", True, self.player2.farge)
        surface.blit(p2_tekst, (1100, 600))

        #tegner Livene
        for i in range(self.player1.liv): #brukte chat på hvordan tegne livene
            pygame.draw.circle(surface, self.player1.farge, (100 + i * 35, 580), 12)
        for i in range(self.player2.liv):
            pygame.draw.circle(surface, self.player2.farge, (1100 + i * 35, 580), 12)

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

        # generelt
        self.navn = navn
        self.farge = farge
        self.font = pygame.font.SysFont("Times new roman", 60, bold = True)
        self.karakter = karakter
        self.timer = 0  # fikk påmåte ideen fra chat, men brukte den på en annen måte

        # bevegelse
        self.speed = 7
        self.vy = 0
        self.vx = 0
        self.på_bakken = False
        self.antall_hopp = 0
        self.max_hopp = 2
        self.kontroller = kontroller
        self.invincibility = False
        self.dodge_cooldown = 0
        self.dodge_frames = 0

        # Attacks & special
        self.attack_retning = 1 #<-- chat på denne
        self.attack_cooldown = 0
        self.melee_rect = None  # <- chat
        self.melee_attack_varer = 0
        self.melee_traff = False
        self.knockback_siden = 0
        self.charge_timer = 0
        self.special_traff = False
        self.special_cooldown = 0

        # liv
        self.død = False
        self.timer_død = 0
        self.død_x = 0
        self.død_y = 0
        self.hp = 0
        self.liv = 3
        self.spawn_x = x
        self.spawn_y = y
        
        # Bilder & Lyd
        self.bilde = pygame.image.load(bilde)
        self.bilde = pygame.transform.scale(self.bilde, (bredde, høyde))

        self.promp = pygame.mixer.Sound("assets/lyder/promp.mp3")
        self.dash_lyd = pygame.mixer.Sound("assets/lyder/dash_lyd.mp3")

        # Ekstra
        self.birk_special_bool = False
        self.birk_special_bool_ned = False
        self.birk_special_bool_lyd = False
        self.doom_special_bool = False
        self.doom_special_bool_lyd = False
        self.herman_special_bool = False
        self.prosjektil_rect = None



    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Hopp
            if event.key == self.kontroller["up"]:
                if self.på_bakken == True or self.antall_hopp < self.max_hopp:
                    self.vy = -8
                    self.på_bakken = False
                    self.antall_hopp += 1

            # Melee/ basic attack
            if event.key == self.kontroller["attack"] and self.attack_cooldown <= 0:
                if self.karakter == "birk":
                    self.attack_cooldown = 90
                    self.melee_attack_varer = 20
                else:
                    self.attack_cooldown = 45
                    self.melee_attack_varer = 20

            # Dodge & Dash
            if event.key == self.kontroller["Dodge"] and self.dodge_cooldown <= 0 and self.knockback_siden == 0:
                self.invincibility = True
                self.dodge_frames = 25
                self.dodge_cooldown = 120
                self.dash_lyd.play()
                if self.attack_retning == 1:
                    self.knockback_siden = 18
                else:
                    self.knockback_siden = -18


    def respawn(self):
        # Resetter stats og setter posisjon til spiller
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.hp = 0
        self.vy = 0
        self.knockback_siden = 0
        self.på_bakken = False
        

    def knockback(self, retning, damage):
        # Regner ut hvor mye knockback i forhold til damage
        styrke = 4 + damage * 0.9  # mer jo mer % man har. brukte chat for hvordan kalulasjonene skulle gjøres
        self.knockback_siden = styrke * retning
        self.vy = -(0.5 + damage * 0.05)


    def draw(self, screen):
        # Tegner karakterene
        screen.blit(self.bilde, self.rect)
        
        # P1/ P2 tekst over karakterene
        tekst = self.font.render(self.navn, True, self.farge)
        screen.blit(tekst, (self.rect.centerx - tekst.get_width() // 2, self.rect.top - 55)) # chat

        # Døds animasjon på en måte - funka litt dårlig så kommenterte bort
        #if self.død == True:
            #pygame.draw.rect(screen, (235, 165, 20), pygame.Rect(self.død_x, self.død_y, 200, 200))


    def update(self):
        keys = pygame.key.get_pressed()

        #Bevegelse mot sidene og bestemmer siden man attacker mot
        if keys[self.kontroller["left"]]: # chat
            self.rect.x -= self.speed
            self.attack_retning = -1
        if keys[self.kontroller["right"]]: #chat
            self.rect.x += self.speed
            self.attack_retning = 1
        
        #knockback
        self.rect.x += self.knockback_siden # Denne blokken er hovedsaklig Chat
        self.knockback_siden *= 0.85
        if abs(self.knockback_siden) < 0.3:
            self.knockback_siden = 0

        #dodge
        if self.dodge_frames > 0:
            self.dodge_frames -= 1
        else:
            self.invincibility = False

        # teller ned cooldowns
        self.dodge_cooldown -= 1
        self.attack_cooldown -= 1 #vet at den går til minus men det har ingenting å si

        # Melee attack
        if self.melee_attack_varer > 0: #hvor lenge attacket varer, chatt
            self.melee_attack_varer -= 1
            if self.attack_retning == 1:
                self.melee_rect = pygame.Rect(self.rect.right, self.rect.centery-70, 100, 25)
            else:
                self.melee_rect = pygame.Rect(self.rect.left - 100, self.rect.centery-70, 100, 25)
        else:
            self.melee_rect = None
            self.melee_traff = False    

        # Horizontal sjekk på platformen
        for platform in [self.game.spill_bane1, self.game.spill_bane2]: # Denne blokken er Chat
            if self.rect.colliderect(platform):
                if self.rect.centerx < platform.left:
                    self.rect.right = platform.left
                    self.vx = 0
                elif self.rect.centerx > platform.right:
                    self.rect.left = platform.right
                    self.vx = 0

        # Lar karakteren gå raskere ned
        if keys[self.kontroller["down"]]:
            if self.vy <= 0:
                self.vy = 0
            else:
                self.rect.y += 5
    
        # Teller ned special cooldown
        self.special_cooldown -= 1

        # Gravitasjon og friksjon
        self.vy += 0.35
        self.vx *= 0.93

        # flytter karakterene når man går
        self.rect.y += self.vy
        self.rect.x += self.vx

        # Vertikal sjekk på plattformen
        for platform in [self.game.spill_bane1, self.game.spill_bane2]: # hjelp fra chat men skrevet selv
            if self.rect.colliderect(platform):
                if self.vy >= 0:
                    self.rect.bottom = platform.top
                    self.vy = 0
                    self.på_bakken = True
                    self.antall_hopp = 0
                    self.birk_special_bool_ned = False

                elif self.vy < 0:
                    self.rect.top = platform.bottom
                    self.vy = 0
                    self.på_bakken = False

        # Teller ned timer
        if self.timer > 0:
            self.timer -= 1

        if self.timer_død > 1:  # fikk hjep av claude, etter at jeg satt fast lenge med hvordan boksen skulle gå bort(og mer bla bla)
            self.timer_død -= 1
        else:
            if self.død == True:       
                self.respawn()
            self.død = False
        
        if self.rect.x > 0 and self.rect.x < 1295 and self.rect.y < 695:
            self.død_x = self.rect.x
            self.død_y = self.rect.y

        if self.rect.x > 1500 or self.rect.x < -300 or self.rect.y > 1100:
            if self.død == False: # gjør at den bare kjører en gang
                self.promp.play()
                self.liv -= 1
                self.død = True
                self.timer_død = 120
            
            # Sjekker hvem som vinner, og gjør at informasjonen kan bli brukt i neste state
            if self.liv <= 0:
                if self.game.player1 == self: # <--chat hjalp med denne linjen
                    self.game.persist["vinner"] = self.game.player2.karakter
                    self.game.next_state = "END"
                    self.game.done = True
                else:
                    self.game.persist["vinner"] = self.game.player1.karakter
                    self.game.next_state = "END"
                    self.game.done = True 


    def Load_image(self,bilde_navn,scale=None): # https://www.youtube.com/watch?v=u7XpkyemKTo for guide 
        image = pygame.image.load(os.path.join("assets/bilder",bilde_navn))

        if scale is not None:
            image = pygame.transform.scale(image,scale)
        return image


class Doomfist(Player):
    def __init__(self, x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter):
        
        super().__init__(x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter)
        
        self.bilde_d = self.Load_image("Doomfist.png",(100,150)) # Doom
        self.hopp = self.Load_image("doomfist_hopp.png",(100,150))
        self.special = self.Load_image("doom_special.png",(150,200))
        self.attack_h = self.Load_image("doom_attack_høyre.png", (100, 50))
        self.attack_v = self.Load_image("doom_attack_venstre.png", (100, 50))
        self.doom_special_bool = False
        self.doom_special_bool_lyd = False
        self.doom_punch = pygame.mixer.Sound("assets/lyder/Rocket-punch.ogg")
        
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()

        # Special attack (Charger opp og slår hardt og langt til sidene (2.5 sek cooldown))
        if keys[self.kontroller["special"]]  and self.special_cooldown <= 0 and self.doom_special_bool == False:
            self.charge_timer += 1
            if self.charge_timer >= 20:
                self.timer = 30
                self.vx = 35 * self.attack_retning # * self.attack_retning : var chat sin idee
                self.doom_special_bool = True
                self.special_cooldown = 150
        else:
            self.charge_timer = 0

        if self.timer == 1:
            self.vx = 0
        elif self.timer < 1:
            self.doom_special_bool = False
            self.special_traff = False
        
        if self.doom_special_bool == True and self.doom_special_bool_lyd == False:
            self.doom_punch.play()
            self.doom_special_bool_lyd = True
        
        if self.doom_special_bool == True:
            self.bilde = self.special
        elif self.på_bakken == False:
            self.bilde = self.hopp
        else:
            self.bilde = self.bilde_d

    def draw(self, screen):
        super().draw(screen)

        if self.melee_rect:
            if self.attack_retning == 1:
                screen.blit(self.attack_h, self.melee_rect)
            else:
                screen.blit(self.attack_v, self.melee_rect)


class Birk(Player):
    def __init__(self, x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter):
        
        super().__init__(x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter)

        self.bilde_b = self.Load_image("Birk_bein.png",(150,200)) # Birk
        self.hopp = self.Load_image("Birk_hopp.png",(150,200))
        self.special = self.Load_image("Birk_slam_opp.png",(150,200))
        self.special_ned = self.Load_image("Birk_slam_ned.png",(200,200))
        self.attack = self.Load_image("attack_animation_Birk.png",(150,200))
        self.attack_arm = self.Load_image("Birk_attack_arm.png",(100, 50))
        self.attack_arm_v = self.Load_image("Birk_attack_arm_v.png",(100, 50))
        self.birk_special_bool = False
        self.birk_special_bool_ned = False
        self.birk_special_bool_lyd = False
        self.Birk_grunt = pygame.mixer.Sound("assets/lyder/Birk_hopp_lyd.wav")


    def update(self):
        super().update()
        keys = pygame.key.get_pressed()

        # Special attack (Hopper høyt opp og slammer ned med stor fart (2 sek cooldown))
        if keys[self.kontroller["special"]] and self.special_cooldown <= 0:
            self.special_traff = False
            self.vy = -18                
            self.birk_special_bool = True
            self.timer = 80
            self.på_bakken = False
            self.special_cooldown = 120

        if self.timer == 1:
            self.birk_special_bool = False
            self.birk_special_bool_ned = True
            self.vy = 20
        
        if self.birk_special_bool == True and self.birk_special_bool_lyd == False:
            self.Birk_grunt.play()
            self.birk_special_bool_lyd = True

        if self.på_bakken == True:
            self.birk_special_bool_ned = False
            self.birk_special_bool_lyd = False
       
        if self.birk_special_bool == True:
            self.bilde = self.special
        if self.birk_special_bool_ned == True:
            self.bilde = self.special_ned
        elif self.på_bakken == False:
            self.bilde = self.hopp
        else:
            self.bilde = self.bilde_b

    def draw(self, screen):
        super().draw(screen)

        if self.melee_rect:
            if self.attack_retning == 1:
                screen.blit(self.attack_arm, self.melee_rect)
            else:
                screen.blit(self.attack_arm_v, self.melee_rect)
            

class Herman(Player):
    def __init__(self, x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter):
        
        super().__init__(x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter)

        self.bilde_h = self.Load_image("Herman_karakter.png",(100,150)) # Herman
        self.hopp = self.Load_image("herman_hopp.png",(100,150))
        self.special = self.Load_image("herman_special.png",(150,200))
        self.attack_h = self.Load_image("herman_attack_høyre.png", (100, 50))
        self.attack_v = self.Load_image("herman_attack_venstre.png", (100, 50))
        self.spytt = self.Load_image("Spytt.png",(30,20))
        self.herman_special_bool = False
        self.prosjektil_rect = None
        self.prosjektil_retning = 1

        
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()

        # Special attack (Spytter ut en projectile som følger en horisontal retning (2.5 sek cooldown))
        if keys[self.kontroller["special"]] and self.special_cooldown <= 0:
                self.herman_special_bool = True
                self.prosjektil_retning = self.attack_retning
                self.prosjektil_rect = pygame.Rect(self.rect.centerx, self.rect.centery, 30, 20) # hjelp av claude**
                self.timer = 70
                self.special_cooldown = 150

        if self.prosjektil_rect:
            self.prosjektil_rect.x += 12 * self.prosjektil_retning
            if self.timer == 1:
                self.prosjektil_rect = None
                self.special_traff = False
 
        elif self.timer <= 1:
            self.herman_special_bool = False
            self.special_traff = False
       
        if self.herman_special_bool == True:
            self.bilde = self.special
        elif self.på_bakken == False:
            self.bilde = self.hopp
        else:
            self.bilde = self.bilde_h

    def draw(self, screen):
        super().draw(screen)
        
        if self.melee_rect:
            if self.attack_retning == 1:
                screen.blit(self.attack_h, self.melee_rect)
            else:
                screen.blit(self.attack_v, self.melee_rect)

        if self.prosjektil_rect:
            screen.blit(self.spytt, self.prosjektil_rect)