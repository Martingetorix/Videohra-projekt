import pygame #type:ignore
from sys import exit
import numpy as np #type:ignore
angle=1.5
scalar=0
playerv=1#rychlost hráče
debug=False
interacttimer=15

pygame.init()
scr_wh=(576,576)
screen=pygame.display.set_mode((scr_wh))#tuple vyjadřuje výšku a šířku scalar pxl
pygame.display.set_caption("Saxoheist4D")
playerpoz=(scr_wh[0]*0.5,scr_wh[1]*0.5)

class mapbase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\Map_test_2.png").convert_alpha()
        self.rect=self.image.get_rect(center=(scr_wh[0]/2,scr_wh[1]/2))
    def update(self):
        Map_base.draw(screen)
class mapcollisionwall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\Map_test_0.png").convert_alpha()
        self.rect=self.image.get_rect(center=(scr_wh[0]/2,scr_wh[1]/2))
        self.mask=pygame.mask.from_surface(self.image)
    def update(self):
        global scalar
        if pygame.sprite.spritecollide(self,Player_hitbox,False,pygame.sprite.collide_mask):
            scalar=-1
        Map_collisionwall.draw(screen)
class mapwall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\Map_test_1.png").convert_alpha()
        self.rect=self.image.get_rect(center=(scr_wh[0]/2,scr_wh[1]/2))
    def update(self):
        Map_wall.draw(screen)
class playerhitbox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\floor.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(16,16))
        self.rect=self.image.get_rect(midbottom=(playerpoz))
    def update(self):
        global debug
        print(scalar)
        if playerv<1:
            if (time*playerv)%2==0:
                self.poz_change=(-np.cos(angle*np.pi)*scalar,-np.sin(angle*np.pi)*scalar)
                self.rect.centerx+=self.poz_change[0]
                self.rect.centery+=self.poz_change[1]
        else:
            self.poz_change=(-np.cos(angle*np.pi)*scalar*playerv,-np.sin(angle*np.pi)*scalar*playerv)
            self.rect.centerx+=self.poz_change[0]
            self.rect.centery+=self.poz_change[1]
        if debug==True:
            Player_hitbox.draw(screen)
class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("graphics\\player\\Sam-front.png").convert_alpha()
        self.rect=self.image.get_rect(midbottom=(playerpoz))
        #convert_alfa a convert optimalizuje obrázek pro pygame s a bez alfa kanálu respektivě
        RG_I_0=self.image=pygame.image.load("graphics\\player\\player_idle0.png").convert_alpha()
        RG_I_1=self.image=pygame.image.load("graphics\\player\\player_idle1.png").convert_alpha()
        RG_M_0=self.image=pygame.image.load("graphics\\player\\player_right0.png").convert_alpha()
        RG_M_1=self.image=pygame.image.load("graphics\\player\\player_right1.png").convert_alpha()

        UP_I_0=self.image=pygame.image.load("graphics\\player\\player_idle0.png").convert_alpha()
        UP_I_1=self.image=pygame.image.load("graphics\\player\\player_idle1.png").convert_alpha()
        UP_M_0=self.image=pygame.image.load("graphics\\player\\player_up0.png").convert_alpha()
        UP_M_1=self.image=pygame.image.load("graphics\\player\\player_up1.png").convert_alpha()

        LF_I_0=self.image=pygame.image.load("graphics\\player\\player_idle0.png").convert_alpha()
        LF_I_1=self.image=pygame.image.load("graphics\\player\\player_idle1.png").convert_alpha()
        LF_M_0=self.image=pygame.image.load("graphics\\player\\player_left0.png").convert_alpha()
        LF_M_1=self.image=pygame.image.load("graphics\\player\\player_left1.png").convert_alpha()

        DW_I_0=self.image=pygame.image.load("graphics\\player\\player_idle0.png").convert_alpha()
        DW_I_1=self.image=pygame.image.load("graphics\\player\\player_idle1.png").convert_alpha()
        DW_M_0=self.image=pygame.image.load("graphics\\player\\player_down0.png").convert_alpha()
        DW_M_1=self.image=pygame.image.load("graphics\\player\\player_down1.png").convert_alpha()
        
        self.imagelist=[[[LF_I_0,LF_I_1],[LF_M_0,LF_M_1]],[[UP_I_0,UP_I_1],[UP_M_0,UP_M_1]],[[RG_I_0,RG_I_1],[RG_M_0,RG_M_1]],[[DW_I_0, DW_I_1],[DW_M_0, DW_M_1]]]#[[Right[idle frames][movement frames]][Up[...]]
        self.poz_change=(0,0)
    def update(self):
        self.image=self.imagelist[int(angle*2)][int(abs(np.sign(scalar)))][int(time*0.1)%2]#[time*rychlost animace chůze%2]
        if playerv<1:
            if (time*playerv)%2==0:
                self.poz_change=(-np.cos(angle*np.pi)*scalar,-np.sin(angle*np.pi)*scalar)
                self.rect.centerx+=self.poz_change[0]
                self.rect.centery+=self.poz_change[1]
        else:
            self.poz_change=(-np.cos(angle*np.pi)*scalar*playerv,-np.sin(angle*np.pi)*scalar*playerv)
            self.rect.centerx+=self.poz_change[0]
            self.rect.centery+=self.poz_change[1]
        Player_object.draw(screen)

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

time=0
floor= pygame.image.load("graphics\\floor.png")
floor=pygame.transform.scale(floor,(scr_wh))
while True:
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
        scalar-=0.5*np.sign(scalar)# zpomalování pohybu
    pygame.display.update()
    pygame.time.Clock().tick(60)#FPS