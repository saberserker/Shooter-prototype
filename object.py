import pygame
import snd
import math

class Bullet:
        def __init__(self, gamestate, st_pos=[0.0,0.0], st_vel=[0.0,0.0], friend=True):
                self.gamestate = gamestate
		self.xy_pos = st_pos
                self.xy_vel = st_vel
                self.size = (4.0,4.0)
                self.friendly = friend
                self.ttl = 4
                self.color = [55,255,55]
        def update_pos(self):
                self.xy_pos[0] = self.xy_pos[0] + self.xy_vel[0]
                self.xy_pos[1] = self.xy_pos[1] + self.xy_vel[1]
        def bounced_x(self):
                if self.friendly:
                        self.friendly = False
                self.xy_vel[0] = -self.xy_vel[0]
                self.ttl = self.ttl - 1
                self.color = [155,55,55]
        def bounced_y(self):
                if self.friendly:
                        self.friendly = False
                self.xy_vel[1] = -self.xy_vel[1]
                self.ttl = self.ttl - 1
                self.color = [155,0,0]

class P1:
        def __init__(self, gamestate, st_pos=[0.0,0.0], st_vel=[0.0,0.0]):
                self.gamestate = gamestate
                self.xy_pos = st_pos
                self.xy_vel = st_vel
                self.health = 10000
                self.size = (20.0,40.0)
                self.hitbox_size = (18,36)
                prinny = []
                for i in range(7,0,-1):
                        prinny.append(pygame.image.load("prinny/"+str(i)+".png").convert_alpha())
                for i in range(5,-1,-1):
                        prinny.append(pygame.transform.flip(prinny[i],True,False))
                self.sprite = prinny
        def determine_sprite(self):
                roll = int(self.xy_vel[0]/1.3+7)
                if (roll <= 0):
                        roll = 0
                elif (roll > 12):
                        roll = 12
                return self.sprite[roll]
        def sprite_coord(self):
                return (int(self.xy_pos[0]-10),int(self.xy_pos[1]-20))
        def update_pos(self):
                self.xy_pos[0] = (self.xy_pos[0] + self.xy_vel[0])%self.gamestate.x_screen
                self.xy_pos[1] = (self.xy_pos[1] + self.xy_vel[1])%self.gamestate.y_screen
        def update_vel(self,decel,acl):
                self.xy_vel[0] = self.xy_vel[0] * decel + acl[0]
                self.xy_vel[1] = self.xy_vel[1] * decel + acl[1]
        def hurt(self, bull):
                abs_velx = (self.xy_vel[0] - bull.xy_vel[0])**2
                abs_vely = (self.xy_vel[1] - bull.xy_vel[1])**2
                return self.dmg(int(math.sqrt(abs_velx + abs_vely)))
        def dmg(self,dam):
                self.health -= dam
                snd.play_se("sounds/grunt1.ogg",.6)
                return dam
        def get_hitbox(self):
                return pygame.Rect((int(self.xy_pos[0]-9),int(self.xy_pos[1]-18)),self.hitbox_size)

class Monster:
        def __init__(self, gamestate, st_pos=[0.0,0.0], st_vel=[0.0,0.0]):
                self.gamestate = gamestate
		self.xy_pos = st_pos
                self.xy_vel = st_vel
                self.health = 100
                self.size = (80.0,110.0)
                self.hitbox_size = (70,100)
                henry = []
                henry.append(pygame.image.load("henry/1.png").convert_alpha())
                henry.append(pygame.image.load("henry/dead.png").convert())#.convert_alpha())
                #henry.append(pygame.image.load("henry/dead.png").convert())
                self.sprite = henry
                self.corpsetime = 30
        def determine_sprite(self):
                if self.health > 0:
                        return self.sprite[0]
                else:
                        if self.corpsetime == 28:
                                snd.play_se("sounds/scream1.ogg",.3)
                        self.corpsetime -= 1
                        self.sprite[1].set_alpha(int(255*self.corpsetime/30.0))
                        return self.sprite[1]
        def sprite_coord(self):
                return (int(self.xy_pos[0]-10),int(self.xy_pos[1]-20))
        def update_pos(self):
                if self.health > 0:
                        self.xy_pos[0] = (self.xy_pos[0] + self.xy_vel[0])%self.gamestate.x_screen
                        self.xy_pos[1] = (self.xy_pos[1] + self.xy_vel[1])%self.gamestate.y_screen
        def hurt(self, bull):
                abs_velx = (self.xy_vel[0] - bull.xy_vel[0])**2
                abs_vely = (self.xy_vel[1] - bull.xy_vel[1])**2
                hurt = int(math.sqrt(abs_velx + abs_vely))
                snd.play_se("sounds/monsterhurt.ogg",.28)
                self.health -= hurt
                return hurt
        def get_hitbox(self):
                return pygame.Rect((int(self.xy_pos[0]-5),int(self.xy_pos[1]-5)),self.hitbox_size)
