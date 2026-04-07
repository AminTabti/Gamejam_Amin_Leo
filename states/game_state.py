"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""
import os
from states.base_state import BaseState
import pygame

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

        self.hp_bar_font = pygame.font.SysFont("Times new roman", 80, bold = True)

#------------ Chat under-----------------------------------------------
        self.player1 = Player(300, 200, self, kontroller={
        "left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s, "special": pygame.K_c, "attack": pygame.K_x, "Dodge" : pygame.K_v}, 
        bilde=bilde1, bredde=bredde1, høyde=høyde1, navn = ".", farge = (30, 60, 200), karakter = karakter1)

        self.player2 = Player(800, 200, self, kontroller={
        "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN, "special": pygame.K_l, "attack": pygame.K_k, "Dodge" : pygame.K_m}, 
        bilde=bilde2, bredde=bredde2, høyde=høyde2, navn = ".", farge = (255, 0, 0), karakter = karakter2)
    #----------Chat over-----------------------------------


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
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        


    def update(self, dt: float):
        self.player1.update()
        self.player2.update()
        

        if self.player1.melee_rect and self.player1.melee_rect.colliderect(self.player2.rect) and not self.player1.melee_traff and not self.player2.invincibility:
            if self.player1.karakter == "birk":
                self.player2.hp += 8
            else:
                self.player2.hp += 5
            self.player2.knockback(self.player1.attack_retning, self.player2.hp)
            self.player1.melee_traff = True #<-- chat hjalp med hvordan treffe bare en gang

        if self.player2.melee_rect and self.player2.melee_rect.colliderect(self.player1.rect) and not self.player2.melee_traff and not self.player1.invincibility:
            if self.player2.karakter == "birk":
                self.player1.hp += 8
            else:
                self.player1.hp += 5
            self.player1.knockback(self.player2.attack_retning, self.player1.hp)
            self.player2.melee_traff = True


        if (self.player1.birk_special_bool_ned or self.player1.doom_special_bool or self.player1.herman_special_bool) and not self.player1.special_traff and not self.player2.invincibility:
            if self.player1.rect.colliderect(self.player2.rect):
                self.player2.hp += 20
                self.player2.knockback(self.player1.attack_retning, self.player2.hp)
                self.player1.special_traff = True

        if (self.player2.birk_special_bool_ned or self.player2.doom_special_bool or self.player2.herman_special_bool) and not self.player2.special_traff and not self.player1.invincibility:
            if self.player2.rect.colliderect(self.player1.rect):
                self.player1.hp += 20
                self.player1.knockback(self.player2.attack_retning, self.player1.hp)
                self.player2.special_traff = True


        if self.player1.prosjektil_rect and not self.player1.special_traff and not self.player2.invincibility:
            if self.player1.prosjektil_rect.colliderect(self.player2.rect):
                self.player2.hp += 5
                self.player2.knockback(self.player1.attack_retning, self.player2.hp)
                self.player1.special_traff = True
        if self.player2.prosjektil_rect and not self.player2.special_traff and not self.player1.invincibility:
            if self.player2.prosjektil_rect.colliderect(self.player1.rect):
                self.player1.hp += 5
                self.player1.knockback(self.player2.attack_retning, self.player1.hp)
                self.player2.special_traff = True


    def draw(self, surface: pygame.Surface):
        surface.blit(self.bakgrunn, (0,0))
        pygame.draw.rect(surface, (255, 0, 0), self.spill_bane1, 2)
        pygame.draw.rect(surface, (255, 0, 0), self.spill_bane2, 2)

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

        #generelt
        self.navn = navn
        self.farge = farge
        self.font = pygame.font.SysFont("Times new roman", 200)
        self.karakter = karakter
        self.timer = 10000000  # fikk påmåte ideen fra chat, men brukte den på en annen måte

        #bevegelse
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

        #Attacks & special
        self.attack_retning = 1 #<-- chat på denne
        self.attack_cooldown = 0
        self.melee_rect = None  # <- chat
        self.melee_attack_varer = 0
        self.melee_traff = False
        self.knockback_siden = 0
        self.charge_timer = 0


        self.special_traff = False
        self.special_cooldown = 0
        self.herman_special_bool = False # herman
        self.doom_special_bool = False # Doom
        self.doom_special_bool_lyd = False
        
        self.birk_special_bool = False # Birk
        self.birk_special_bool_ned = False
        self.birk_attack_bool = False
        self.birk_special_bool_lyd = False

        #liv
        self.død = False
        self.timer_død = 0
        self.død_x = 0
        self.død_y = 0

        self.hp = 0
        self.liv = 3
        self.spawn_x = x
        self.spawn_y = y
        
        #Bilder & Lyd
        self.bilde = pygame.image.load(bilde)
        self.bilde = pygame.transform.scale(self.bilde, (bredde, høyde))

        self.promp = pygame.mixer.Sound("assets/promp.mp3")
        self.Birk_grunt = pygame.mixer.Sound("assets/Birk_hopp_lyd.wav")
        self.doom_punch = pygame.mixer.Sound("assets/Rocket-punch.ogg")
        self.dash_lyd = pygame.mixer.Sound("assets/dash_lyd.mp3")


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.kontroller["up"]:  # brukte chat for å finne ut hvordan gjøre at den ikke holdes inne
                if self.på_bakken or self.antall_hopp < self.max_hopp:
                    self.vy = -8
                    self.på_bakken = False
                    self.antall_hopp += 1

            if event.key == self.kontroller["attack"] and self.attack_cooldown <= 0:
                if self.karakter == "birk":
                    self.attack_cooldown = 90
                    self.melee_attack_varer = 20
                else:
                    self.attack_cooldown = 45
                    self.melee_attack_varer = 20
            
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
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.hp = 0
        self.vy = 0
        self.knockback_siden = 0
        self.på_bakken = False
        

    def knockback(self, retning, damage):
        styrke = 4 + damage * 0.9  # mer jo mer % man har. brukte chat for hvordan kalulasjonene skulle gjøres
        self.knockback_siden = styrke * retning
        self.vy = -(0.5 + damage * 0.05)


    def draw(self, screen):
        screen.blit(self.bilde, self.rect)
        
        tekst = self.font.render(self.navn, True, self.farge)
        screen.blit(tekst, (self.rect.centerx - tekst.get_width() // 2, self.rect.top - 185)) # chat

        if self.melee_rect:
            if self.karakter == "herman":
                if self.attack_retning == 1:
                    screen.blit(self.herman_attack_h, self.melee_rect)
                else:
                    screen.blit(self.herman_attack_v, self.melee_rect)

            if self.karakter == "doomfist":
                if self.attack_retning == 1:
                    screen.blit(self.doom_attack_h, self.melee_rect)
                else:
                    screen.blit(self.doom_attack_v, self.melee_rect)

            if self.karakter == "birk":
                if self.attack_retning == 1:
                    screen.blit(self.birk_attack_arm, self.melee_rect)
                else:
                    screen.blit(self.birk_attack_arm_v, self.melee_rect)


            #pygame.draw.rect(screen, (255, 165, 0), self.melee_rect)
            

        if self.død == True:
            pygame.draw.rect(screen, (255, 165, 0), pygame.Rect(self.død_x, self.død_y, 1000, 1000))

        if self.herman_special_bool == True:
            #pygame.draw.rect(screen, (255,165, 0),pygame.Rect(self.rect.x, self.rect.y, 500, 500))
            if self.prosjektil_rect:
                screen.blit(self.spytt, self.prosjektil_rect)


    def update(self):
        keys = pygame.key.get_pressed()

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


        self.dodge_cooldown -= 1
        self.attack_cooldown -= 1 #vet at den går til minus men det har ingenting å si


        if self.melee_attack_varer > 0: #hvor lenge attacket varer, chatt
            self.melee_attack_varer -= 1
            if self.attack_retning == 1:
                self.melee_rect = pygame.Rect(self.rect.right, self.rect.centery-70, 100, 25)
            else:
                self.melee_rect = pygame.Rect(self.rect.left - 100, self.rect.centery-70, 100, 25)
        else:
            self.melee_rect = None
            self.melee_traff = False    


        if keys[self.kontroller["special"]] and self.special_cooldown <= 0:
             # mellom 6 og 7 sekunder :) XD

            if self.karakter == "birk":
                self.vy = -18                
                self.birk_special_bool = True
                self.timer = 80
                self.på_bakken = False
                self.special_cooldown = 100 
            
            elif self.karakter == "herman":
                self.herman_special_bool = True
                self.prosjektil_rect = pygame.Rect(self.rect.centerx, self.rect.centery, 30, 20) # hjelp av claude**
                self.timer = 80
                self.special_cooldown = 100 
                
        if keys[self.kontroller["special"]] and self.karakter == "doomfist" and self.special_cooldown <= 0:
            self.charge_timer += 1
            if self.charge_timer >= 60:
                self.timer = 80
                self.vx = 35
                self.doom_special_bool = True
                self.special_cooldown = 100  # mellom 6 og 7 sekunder :) XD
        else:
            self.charge_timer = 0

        self.special_cooldown -= 1
       

        if self.timer == 1:
            self.vy = 20

            if self.karakter == "birk":
                self.birk_special_bool = False
                self.birk_special_bool_ned = True

            elif self.karakter == "doomfist":
                self.doom_special_bool = False

            elif self.karakter == "herman":
                self.herman_special_bool = False

        if self.på_bakken == True:
            self.birk_special_bool_ned = False
            self.birk_special_bool_lyd = False
            #self.doom_special_bool = False
            #self.herman_special_bool = False     
         

        for platform in [self.game.spill_bane1, self.game.spill_bane2]: #Horizontal sjekken. Denne blokken er Chat
            if self.rect.colliderect(platform):
                if self.rect.centerx < platform.left:
                    self.rect.right = platform.left
                elif self.rect.centerx > platform.right:
                    self.rect.left = platform.right


        if keys[self.kontroller["down"]]:
            if self.vy <= 0:
                self.vy = 0

            else:
                self.rect.y += 5
    

        self.vy += 0.35


        self.vx *= 0.93


        self.rect.y += self.vy
        self.rect.x += self.vx


        for platform in [self.game.spill_bane1, self.game.spill_bane2]: # hjelp fra chat men skrevet selv
            if self.rect.colliderect(platform):
                if self.vy >= 0:
                    self.rect.bottom = platform.top
                    self.vy = 0
                    self.på_bakken = True
                    self.antall_hopp = 0
                    self.birk_special_bool_ned = False

                if self.karakter == "birk":
                    self.special_traff = False

                elif self.vy < 0:
                    self.rect.top = platform.bottom
                    self.vy = 0
                    self.på_bakken = False


        self.timer -= 1


        if self.timer_død > 1:  # fikk hjep av claude, etter at jeg satt fast lenge med hvordan boksen skulle gå bort(og mer bla bla)
            self.timer_død -= 1

        else:
            if self.død == True:       
                self.respawn()
            self.død = False
        
        if self.karakter == "birk":
            self.update_image_Birk()
            self.update_lyd_Birk()

        if self.karakter == "doomfist":
            self.update_image_doomfist()
            self.update_lyd_doomfist()

        if self.karakter == "herman":
            self.update_image_herman()
        
        if self.prosjektil_rect:
            self.prosjektil_rect.x += 12 * self.attack_retning
            if self.timer == 0:
                self.prosjektil_rect = None
                self.special_traff = False
        
 
        if self.rect.x > 0 and self.rect.x < 1295 and self.rect.y < 695:
            self.død_x = self.rect.x
            self.død_y = self.rect.y

        if self.rect.x > 1800 or self.rect.x < -500 or self.rect.y > 1100:
            if self.død == False: # gjør at den bare kjører en gang
                self.promp.play()
                self.liv -= 1
                self.død = True
                self.timer_død = 120
            
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
        image = pygame.image.load(os.path.join("assets",bilde_navn))

        if scale is not None:
            image = pygame.transform.scale(image,scale)
        return image
    

    def update_image_Birk(self):
        if self.på_bakken == False:
           self.bilde = self.birk_hopp

        if self.birk_special_bool == True:
            self.bilde = self.birk_special

        if self.birk_special_bool_ned == True:
            self.bilde = self.birk_special_ned

        if self.på_bakken == True:
            self.bilde = self.birk_bilde

        if self.melee_attack_varer > 0:
            self.bilde = self.birk_attack
    

    def update_image_doomfist(self):
        if self.på_bakken == False:
           self.bilde = self.doom_hopp

        if self.doom_special_bool == True:
            self.bilde = self.doom_special

        if self.på_bakken == True and self.doom_special_bool == False:
            self.bilde = self.doom_bilde
    

    def update_image_herman(self):
        if self.på_bakken == False:
           self.bilde = self.herman_hopp

        if self.herman_special_bool == True:
            self.bilde = self.herman_special

        if self.på_bakken == True:
            self.bilde = self.herman_bilde


    def update_lyd_Birk(self):
        if self.birk_special_bool == True and self.birk_special_bool_lyd == False:
            self.Birk_grunt.play()
            self.birk_special_bool_lyd = True

    def update_lyd_doomfist(self):
        if self.doom_special_bool == True and self.doom_special_bool_lyd == False:
            self.doom_punch.play()
            self.doom_special_bool_lyd = True

    def update_lyd_Herman(self):
        pass
class Doomfist(Player):
    def __init__(self, x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter):
        self.game = game
        super().__init__(x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter)
        
        self.bilde = self.Load_image("Doomfist.png",(100,150)) # Doom
        self.hopp = self.Load_image("doomfist_hopp.png",(100,150))
        self.special = self.Load_image("doom_special.png",(150,200))
        self.attack_h = self.Load_image("doom_attack_høyre.png", (100, 50))
        self.attack_v = self.Load_image("doom_attack_venstre.png", (100, 50))
        
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if self.vx < 0.001: # gjør at man kan treffe pånytt
            self.special_traff = False

        if keys[self.kontroller["special"]]  and self.special_cooldown <= 0:
            self.charge_timer += 1
            if self.charge_timer >= 60:
                self.timer = 80
                self.vx = 35
                self.doom_special_bool = True
                self.special_cooldown = 100  # mellom 6 og 7 sekunder :) XD
        else:
            self.charge_timer = 0
        self.update_image_doomfist()
        self.update_lyd_doomfist()
        if self.timer == 1:
            self.doom_special_bool = False




class Birk(Player):
    def __init__(self, x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter):
        self.game = game
        super().__init__(x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter)
        self.birk_bilde = self.Load_image("Birk_bein.png",(150,200)) # Birk
        self.birk_hopp = self.Load_image("Birk_hopp.png",(150,200))
        self.birk_special = self.Load_image("Birk_slam_opp.png",(150,200))
        self.birk_special_ned = self.Load_image("Birk_slam_ned.png",(200,200))
        self.birk_attack = self.Load_image("attack_animation_Birk.png",(150,200))
        self.birk_attack_arm = self.Load_image("Birk_attack_arm.png",(100, 50))
        self.birk_attack_arm_v = self.Load_image("Birk_attack_arm_v.png",(100, 50))
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[self.kontroller["special"]] and self.special_cooldown <= 0:
            self.vy = -18                
            self.birk_special_bool = True
            self.timer = 80
            self.på_bakken = False
            self.special_cooldown = 100 
    def handle_event(self, event):
        super().handle_event(event)
        if event.key == self.kontroller["attack"] and self.attack_cooldown <= 0:
                if self.karakter == "birk":
                    self.attack_cooldown = 90
                    self.melee_attack_varer = 20



class Herman(Player):
    def __init__(self, x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter):
        self.game = game
        super().__init__(x, y, game, kontroller, bilde, bredde, høyde, navn, farge, karakter)

        self.bilde = self.Load_image("Herman_karakter.png",(100,150)) # Herman
        self.hopp = self.Load_image("herman_hopp.png",(100,150))
        self.special = self.Load_image("herman_special.png",(150,200))
        self.attack_h = self.Load_image("herman_attack_høyre.png", (100, 50))
        self.attack_v = self.Load_image("herman_attack_venstre.png", (100, 50))
        self.spytt = self.Load_image("Spytt.png",(30,20))

        self.prosjektil_rect = None
        
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()

        if keys[self.kontroller["special"]] and self.special_cooldown <= 0:
                self.herman_special_bool = True
                self.prosjektil_rect = pygame.Rect(self.rect.centerx, self.rect.centery, 30, 20) # hjelp av claude**
                self.timer = 80
                self.special_cooldown = 100 