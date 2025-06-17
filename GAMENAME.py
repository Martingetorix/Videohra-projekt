import pygame #type:ignore
from sys import exit
import numpy as np #type:ignore
import math

angle=1.5
scalar=0
playerv=1 #rychlost hráče
debug=True
interacttimer=15
pygame.init()


pygame.init()
scr_wh=(576,576)
screen=pygame.display.set_mode((scr_wh)) #tuple vyjadřuje výšku a šířku scalar pxl
pygame.display.set_caption("Saxoheist4D")
playerpoz=(scr_wh[0]*0.5,scr_wh[1]*0.5)

def color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

class mapbase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\Map_test_2.png").convert_alpha()
        self.rect=self.image.get_rect(center=(scr_wh[0]/2,scr_wh[1]/2))
    def update(self):
        screen.blit(self.image, self.rect)

class mapcollisionwall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\Map_test_0.png").convert_alpha()
        self.rect=self.image.get_rect(center=(scr_wh[0]/2,scr_wh[1]/2))
        self.mask=pygame.mask.from_surface(self.image)
    def update(self):
        global scalar
        global angle
        ph = Player_hitbox.sprite #Tady řešíme kolizi s konkrétním hitboxem a setneme angle pohybu opačně k dané stěně
        if self.mask.overlap_area(pygame.mask.Mask((ph.rect_top.width, ph.rect_top.height), fill=True), (ph.rect_top.x - self.rect.x, ph.rect_top.y - self.rect.y)):
            angle = 1.5
        if self.mask.overlap_area(pygame.mask.Mask((ph.rect_bottom.width, ph.rect_bottom.height), fill=True), (ph.rect_bottom.x - self.rect.x, ph.rect_bottom.y - self.rect.y)):
            angle = 0.5
        if self.mask.overlap_area(pygame.mask.Mask((ph.rect_left.width, ph.rect_left.height), fill=True), (ph.rect_left.x - self.rect.x, ph.rect_left.y - self.rect.y)):
            angle = 1
        if self.mask.overlap_area(pygame.mask.Mask((ph.rect_right.width, ph.rect_right.height), fill=True), (ph.rect_right.x - self.rect.x, ph.rect_right.y - self.rect.y)):
            angle = 0
        Map_collisionwall.draw(screen)

class mapwall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\Map_test_1.png").convert_alpha()
        self.rect=self.image.get_rect(center=(scr_wh[0]/2,scr_wh[1]/2))
    def update(self):
        screen.blit(self.image, self.rect)

class playerhitbox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\floor.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(8,8))
        #vytváří hlavní hitbox
        self.rect = self.image.get_rect(center=playerpoz)
        #vytváří obdelníky kolem hlavního hitboxu vlevo a vpravo mají prohozenou délku a šířku:
        self.rect_top = pygame.Rect(0, 0, 8, 2) 
        self.rect_top.midbottom = self.rect.midtop

        self.rect_bottom = pygame.Rect(0, 0, 8, 2)
        self.rect_bottom.midtop = self.rect.midbottom

        self.rect_left = pygame.Rect(0, 0, 2, 8)
        self.rect_left.midright = self.rect.midleft

        self.rect_right = pygame.Rect(0, 0, 2, 8)
        self.rect_right.midleft = self.rect.midright
    def update(self):
        global debug
        # print(scalar)
        if playerv < 1: #Magie co sem dal Martin
            if (time * playerv) % 2 == 0:
                self.poz_change = (-np.cos(angle * np.pi) * scalar, -np.sin(angle * np.pi) * scalar)
                self.rect.centerx += self.poz_change[0]
                self.rect.centery += self.poz_change[1]
        else:
            self.poz_change = (-np.cos(angle * np.pi) * scalar * playerv, -np.sin(angle * np.pi) * scalar * playerv)
            self.rect.centerx += self.poz_change[0]
            self.rect.centery += self.poz_change[1]

    # Tohle umisťuje pomocný hitboxy kolem hlavního
        self.rect_top.midbottom = self.rect.midtop
        self.rect_bottom.midtop = self.rect.midbottom
        self.rect_left.midright = self.rect.midleft
        self.rect_right.midleft = self.rect.midright

        if debug: #tohle vykreslí hitboxy je-li zapnutý debug
            pygame.draw.rect(screen, (0, 0, 0), self.rect_top, 1)
            pygame.draw.rect(screen, (0, 0, 0), self.rect_bottom, 1)
            pygame.draw.rect(screen, (0, 0, 0), self.rect_left, 1)
            pygame.draw.rect(screen, (0, 0, 0), self.rect_right, 1)

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\player\\Sam-front.png").convert_alpha()
        self.rect=self.image.get_rect(midbottom=(playerpoz))
        RG_I_0=pygame.image.load("graphics\\player\\player_idle0.png").convert_alpha()
        RG_I_1=pygame.image.load("graphics\\player\\player_idle1.png").convert_alpha()
        RG_M_0=pygame.image.load("graphics\\player\\player_right0.png").convert_alpha()
        RG_M_1=pygame.image.load("graphics\\player\\player_right1.png").convert_alpha()

        UP_I_0=pygame.image.load("graphics\\player\\player_idle0.png").convert_alpha()
        UP_I_1=pygame.image.load("graphics\\player\\player_idle1.png").convert_alpha()
        UP_M_0=pygame.image.load("graphics\\player\\player_up0.png").convert_alpha()
        UP_M_1=pygame.image.load("graphics\\player\\player_up1.png").convert_alpha()

        LF_I_0=pygame.image.load("graphics\\player\\player_idle0.png").convert_alpha()
        LF_I_1=pygame.image.load("graphics\\player\\player_idle1.png").convert_alpha()
        LF_M_0=pygame.image.load("graphics\\player\\player_left0.png").convert_alpha()
        LF_M_1=pygame.image.load("graphics\\player\\player_left1.png").convert_alpha()

        DW_I_0=pygame.image.load("graphics\\player\\player_idle0.png").convert_alpha()
        DW_I_1=pygame.image.load("graphics\\player\\player_idle1.png").convert_alpha()
        DW_M_0=pygame.image.load("graphics\\player\\player_down0.png").convert_alpha()
        DW_M_1=pygame.image.load("graphics\\player\\player_down1.png").convert_alpha()
        
        self.imagelist=[[[LF_I_0,LF_I_1],[LF_M_0,LF_M_1]],[[UP_I_0,UP_I_1],[UP_M_0,UP_M_1]],[[RG_I_0,RG_I_1],[RG_M_0,RG_M_1]],[[DW_I_0, DW_I_1],[DW_M_0, DW_M_1]]]
        self.poz_change=(0,0)
    def update(self):
        self.image=self.imagelist[int(angle*2)][int(abs(np.sign(scalar)))][int(time*0.1)%2]
        if playerv<1:
            if (time*playerv)%2==0:
                self.poz_change=(-np.cos(angle*np.pi)*scalar,-np.sin(angle*np.pi)*scalar)
                self.rect.centerx+=self.poz_change[0]
                self.rect.centery+=self.poz_change[1]
        else:
            self.poz_change=(-np.cos(angle*np.pi)*scalar*playerv,-np.sin(angle*np.pi)*scalar*playerv)
            self.rect.centerx+=self.poz_change[0]
            self.rect.centery+=self.poz_change[1]
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, path_points, speed=1):
        super().__init__()
        self.images = [pygame.image.load("graphics\\enemy.png").convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=path_points[0])
        self.path = path_points
        self.current_point = 1
        self.speed = speed
        self.time_counter = 0
        
        self.light_angle = math.radians(60)  
        self.light_length = 150  
        self.direction = pygame.math.Vector2(1, 0)  
        
    def update(self):
        if not self.path:
            return
        

        target = self.path[self.current_point]
        dx = target[0] - self.rect.centerx
        dy = target[1] - self.rect.centery
        dist = np.hypot(dx, dy)
        
        if dist < self.speed:
            self.current_point = (self.current_point + 1) % len(self.path)
            next_target = self.path[self.current_point]
            direction_vector = pygame.math.Vector2(next_target[0] - self.rect.centerx, next_target[1] - self.rect.centery)
            if direction_vector.length() != 0:
                self.direction = direction_vector.normalize()
        else:
            dx, dy = dx / dist, dy / dist
            self.rect.centerx += dx * self.speed
            self.rect.centery += dy * self.speed
            self.direction = pygame.math.Vector2(dx, dy)
        
        self.time_counter += 1
        self.image = self.images[(self.time_counter // 30) % len(self.images)]
        
        screen.blit(self.image, self.rect)
        self.draw_light_cone()
        self.check_player_in_light()

    def draw_light_cone(self):
        start_pos = pygame.math.Vector2(self.rect.center)


        rays = []
        ray_count = 30  

        for i in range(ray_count + 1):
            angle_offset = -self.light_angle / 2 + (self.light_angle * i / ray_count)
            direction = self.direction.rotate_rad(angle_offset)
            end_point = self.cast_ray(start_pos, direction)
            rays.append(end_point)

       
        s = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(s, (255, 255, 0, 100), [start_pos] + rays)
        screen.blit(s, (0, 0))

    def cast_ray(self, start_pos, direction):
        max_length = self.light_length
        step = 2

        for i in range(0, int(max_length), step):
            check_pos = start_pos + direction * i
            x, y = int(check_pos.x), int(check_pos.y)

            if 0 <= x < scr_wh[0] and 0 <= y < scr_wh[1]:
                if Map_collisionwall.sprite.mask.get_at((x - Map_collisionwall.sprite.rect.left,
                                                         y - Map_collisionwall.sprite.rect.top)):
                    return (x, y)
            else:
                break

        return (int(start_pos.x + direction.x * max_length),
                int(start_pos.y + direction.y * max_length))

    def check_player_in_light(self):
        player_pos = pygame.math.Vector2(Player_hitbox.sprite.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        vec_to_player = player_pos - enemy_pos

        if vec_to_player.length() > self.light_length:
            return

        vec_to_player_norm = vec_to_player.normalize()
        angle_between = self.direction.angle_to(vec_to_player_norm)

        if abs(angle_between) <= math.degrees(self.light_angle / 2):
            
            hit_point = self.cast_ray(enemy_pos, vec_to_player_norm)
            if (int(player_pos.x), int(player_pos.y)) == (int(hit_point[0]), int(hit_point[1])):
                print("Prohra! Hráč je v kuželu světla a není za zdí!")

class ReactivePlace:
    def __init__(self, x, y, sirka, vyska):
        self.rect = pygame.Rect(x, y, sirka, vyska)
        self.aktivni = False
        self.barva = (255, 0, 0)  # výchozí barva - červená (neaktivní)

    def zkontroluj_kolizi(self, hrac_rect):
        if self.rect.colliderect(hrac_rect) and not self.aktivni:
            self.aktivni = True
            self.barva = (0, 255, 0)  # aktivní barva - zelená
            print("abc")
    
    def vykresli(self, povrch):
        """Vykreslí místo na obrazovku."""
        pygame.draw.rect(povrch, self.barva, self.rect)

class Button():  # toto je zkopírováno
    def __init__(self, image, pos, image_new):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.image_new = image_new
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.image_new
        else:
            self.image = self.image

Player_object=pygame.sprite.GroupSingle()
Player_object.add(player())        
Player_hitbox=pygame.sprite.GroupSingle()
Player_hitbox.add(playerhitbox())
Map_base=pygame.sprite.GroupSingle()
Map_base.add(mapbase())   
Map_wall=pygame.sprite.GroupSingle()
Map_wall.add(mapwall())   
Map_collisionwall=pygame.sprite.GroupSingle()
Map_collisionwall.add(mapcollisionwall()) 


Enemies = pygame.sprite.Group()
enemy_path = [(50, 50), (100, 100), (150, 150), (400, 150)]  
enemy = Enemy(enemy_path, speed=1.2)
Enemies.add(enemy)
reactive_place = ReactivePlace(64, 64, 64, 64)
time=0

floor= pygame.image.load("graphics\\floor.png")
floor=pygame.transform.scale(floor,(scr_wh))






background = pygame.image.load("graphics\\background.png")
background_levels = pygame.image.load("graphics\\background_levels.png")
background_dead = pygame.image.load("graphics\\background_dead.png")
def dead():
    global game_active
    pygame.display.set_caption('YOU GOT CAUGHT - Saxoheist4D')
    
    while True:
        
        game_active = False
        screen.blit(background_dead, (0, 0))
        
        DEAD_MOUSE_POS = pygame.mouse.get_pos()

        DEAD_BACK = Button(image=pygame.image.load("graphics\\buttons\\back_button.png"), pos=(288, 460), image_new=pygame.image.load("graphics\\buttons\\back_button_new.png"))
                            

        DEAD_BACK.changeColor(DEAD_MOUSE_POS)
        DEAD_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DEAD_BACK.checkForInput(DEAD_MOUSE_POS):
                    return
        pygame.display.update()

def levels():
    pygame.display.set_caption('LEVELS - Saxoheist4D')
    while True:
        
        screen.blit(background_levels, (0, 0))
        
        LEVELS_MOUSE_POS = pygame.mouse.get_pos()

        LEVELS_BACK = Button(image=pygame.image.load("graphics\\buttons\\back_button.png"), pos=(288, 460), image_new=pygame.image.load("graphics\\buttons\\back_button_new.png"))
                            

        LEVELS_BACK.changeColor(LEVELS_MOUSE_POS)
        LEVELS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVELS_BACK.checkForInput(LEVELS_MOUSE_POS):
                    menu()
        pygame.display.update()


def play_loop(): # herní smyčka
    global game_active, time, scalar, angle, interacttimer, debug
    game_active = True
    while game_active:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                exit()
        
        time+=1
        keys=pygame.key.get_pressed()
        if interacttimer>0:
            interacttimer-=1
        elif keys[pygame.K_p]:
            interacttimer=15
            if debug==True:
                debug=False
            else:
                debug=True
        if keys[pygame.K_w] and keys[pygame.K_d]:
            scalar=1
            angle=0.75
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            scalar=1
            angle=0.25
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            scalar=1
            angle=1.25
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            scalar=1
            angle=1.75

        elif keys[pygame.K_w]:
            scalar=1
            angle=0.5
        elif keys[pygame.K_d]:
            scalar=1
            angle=1
        elif keys[pygame.K_s]:
            scalar=1
            angle=1.5
        elif keys[pygame.K_a]:
            scalar=1
            angle=0

        screen.blit(floor,(0,0))
        Map_base.update()
        Map_collisionwall.update()
        Player_object.update()
        Player_hitbox.update()
        Map_wall.update()
        if abs(scalar)>0:
            scalar-=0.5*np.sign(scalar)

        # --- UPDATE A VYKRESLENÍ NEPŘÁTEL ---
        Enemies.update()
        # už nepoužíváme Enemies.draw(screen), protože každý enemy vykresluje sám ve svém update()

        # --- KOLIZE NEPŘÍTEL S HRÁČEM (DETEKCE) ---
        for enemy in Enemies:
            if enemy.rect.colliderect(Player_hitbox.sprite.rect):
                print('byl jsi chycen')
                dead()
                return
                        
        reactive_place.zkontroluj_kolizi(Player_hitbox.sprite.rect)
        reactive_place.vykresli(screen)
        pygame.display.update()
        
    

def menu():
    pygame.display.set_caption('MENU - Saxoheist4D')
    while True:
        screen.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

    
        PLAY_BUTTON = Button(image=pygame.image.load("graphics\\buttons\\play_button.png"), pos=(288, 220), image_new=pygame.image.load("graphics\\buttons\\play_button_new.png")) 
                        
        LEVELS_BUTTON = Button(image=pygame.image.load("graphics\\buttons\\levels_button.png"), pos=(288, 350), image_new=pygame.image.load("graphics\\buttons\\levels_button_new.png")) 
                            
        QUIT_BUTTON = Button(image=pygame.image.load("graphics\\buttons\\quit_button.png"), pos=(288, 480), image_new=pygame.image.load("graphics\\buttons\\quit_button_new.png")) 
                           


        for button in [PLAY_BUTTON, LEVELS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_loop()
                if LEVELS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    levels()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    exit()

        pygame.display.update()

menu()
