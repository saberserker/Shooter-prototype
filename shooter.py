import pygame as py
import math
import random as rnd
import sys
sys.path.insert(0, ".")

import snd
from object import *

def add_list(a,b): #both lists should be of equal size
	retlist = []
	for i in range(len(a)):
		retlist.append(a[i]+b[i])
	return retlist

def cast_int(somelist):
	retlist = []
	for i in somelist:
		retlist.append(int(i))
	return retlist

class Gamestate:
	def __init__(self):
		self.decel = .5  #self.deceleration_constant
		self.accel = 4.0 ##self.acceleration_constant 
		self.bspeed = 10.0

		self.x_screen = 800
		self.y_screen = 500
		self.screensize = (self.x_screen,self.y_screen)
		py.init()
		self.rect_screen = py.Rect((0,0,self.x_screen,self.y_screen))
		self.font = py.font.Font("CooperB.ttf",13)
		self.screen = py.display.set_mode(self.screensize)
		self.clock = py.time.Clock()
		self.backgnd = py.image.load("background/%d.png" % rnd.choice(range(1,7)))
		self.xyplayer_acl = [0.0,0.0]
		self.p1 = P1(self,[self.x_screen/2.0,self.y_screen*8.0/9.0],[0.0,0.0])

		self.bullets = []
		self.monsters = []
		loner = Monster(self,[self.x_screen*8.0/9.0,self.y_screen/2.0],[-2.0,0.0])
		self.monsters.append(loner)
		self.shooting = False
		self.over = False
		self.redness = 0
		self.monster_gentime = 100
		self.score = 0

		self.stringstat = [" "," "," "," "]
		snd.play_music("music/%d.ogg" % rnd.choice([1,2,3]),-1,0.6)
		self.loop()



	def loop(self):
		while not self.over:
			self.clock.tick(60)
			self.screen.blit(self.backgnd,(0,0))
			if self.redness > 0:
		#		self.screen.fill((0,self.redness,self.redness),None,py.BLEND_SUB)
				self.screen.fill((self.redness,0,0),None,py.BLEND_ADD)
				#self.screen.fill((255,255-self.redness,255-self.redness))
			#draw player
			self.p1spr = self.p1.determine_sprite()
			self.screen.blit(self.p1spr,self.p1.sprite_coord())
			#draw bullet
			for bull in self.bullets:
				self.screen.fill(bull.color,(cast_int(bull.xy_pos),bull.size))
				#move self.bullets
				bull.update_pos()
			#draw self.monsters
			for mon in self.monsters:
				monspr = mon.determine_sprite()
				self.screen.blit(monspr,mon.sprite_coord())
			#display ingame stats
			self.stringstat[0] = "Health: " + str(int(self.p1.health))
			self.stringstat[1] = "Score: " + str(int(self.score))
			self.stringstat[2] = "FPS: " + str(self.clock.get_fps())
			self.stringstat[3] = "Objects: " + str(len(self.monsters)+len(self.bullets))
			r = []
			r.append(self.font.render(self.stringstat[0], 1, (155, 0,0)))
			r.append(self.font.render(self.stringstat[1], 1, (0, 0,0)))
			r.append(self.font.render(self.stringstat[2], 1, (0, 0,0)))
			r.append(self.font.render(self.stringstat[3], 1, (0, 0,0)))
			self.screen.blit(r[0], (0,0))
			self.screen.blit(r[1], (0,r[0].get_rect()[3]+2))
			self.screen.blit(r[2], (0,r[0].get_rect()[3]*2+4))
			self.screen.blit(r[3], (0,r[0].get_rect()[3]*3+6))
			#move player
			self.p1.update_pos()
			#update velocity
			self.p1.update_vel(self.decel,self.xyplayer_acl)
			#update pain_indicator
			self.redness = int(self.redness*.5)
			#generate monster
			self.monster_gentime -= 1
			if self.monster_gentime <= 0:
				self.monster_gentime = int(rnd.gauss(100,10))
				newmon = Monster(self,[self.x_screen,rnd.randint(0,self.y_screen*0.9)],[-rnd.random()*8.0-3,0.0])
				self.monsters.append(newmon)
			#A held-down button shoots like crazy
			if self.shooting:
				snd.play_se("sounds/gunshot.ogg")
				t = py.mouse.get_pos()
				xy = (t[0] - self.p1.xy_pos[0], t[1] - self.p1.xy_pos[1])
				abs_dist = math.sqrt(xy[0]**2 + xy[1]**2)
				xyvel = (self.bspeed*xy[0]/(abs_dist),self.bspeed*xy[1]/(abs_dist))
				#bullet plus player's speed
				thisbull = Bullet(self,self.p1.xy_pos[:],add_list(xyvel,self.p1.xy_vel))
				self.bullets.append(thisbull)

			self.p1rec = self.p1.get_hitbox()

			#monster behavior
			for mon in self.monsters:
				if mon.corpsetime <= 0 or mon.xy_pos[0] < -80:
					self.monsters.remove(mon)
					self.score += 10
				monrec = mon.get_hitbox()
				if monrec.colliderect(self.p1rec) and mon.health > 0:
					self.p1.dmg(5)
					self.redness += 5 * 10
					if self.redness > 255:
						self.redness = 255
					if self.p1.health <= 0:
						self.over = True
				mon.update_pos()



			#delete self.bullets that left the self.screen....
			#...or instead, bounces them off the wall
			for bull in self.bullets:
				if bull.xy_pos[0] < 0:
					if bull.ttl > 0:
						bull.bounced_x()
						bull.xy_pos[0] = 1
					elif bull in self.bullets: 
						self.bullets.remove(bull)
				elif bull.xy_pos[0] > self.x_screen:
					if bull.ttl > 0:
						bull.bounced_x()
						bull.xy_pos[0] = self.x_screen - 2
					elif bull in self.bullets: 
						self.bullets.remove(bull)
				elif bull.xy_pos[1] < 0:
					if bull.ttl > 0:
						bull.bounced_y()
						bull.xy_pos[1] = 1
					elif bull in self.bullets: 
						self.bullets.remove(bull)
				elif bull.xy_pos[1] > self.y_screen:
					if bull.ttl > 0:
						bull.bounced_y()
						bull.xy_pos[1] = self.y_screen - 2
					elif bull in self.bullets: 
						self.bullets.remove(bull)
				elif self.p1rec.collidepoint(bull.xy_pos):
					if not bull.friendly:
						self.redness += self.p1.hurt(bull) * 4
						if self.redness > 255:
							self.redness = 255
						if self.p1.health < 0:
							self.over = True
						if bull in self.bullets: 
							self.bullets.remove(bull)
				for mon in self.monsters:
					monrec = mon.get_hitbox()
					if monrec.collidepoint(bull.xy_pos):
						if mon.health > 0:
							if bull in self.bullets: 
								self.bullets.remove(bull)
							mon.hurt(bull)
					
						
			
			for e in py.event.get():
				if e.type == py.QUIT:
					self.over = True
				elif e.type == py.KEYDOWN:
					if e.key == py.K_w:
						self.xyplayer_acl[1] += -self.accel
					if e.key == py.K_s:
						self.xyplayer_acl[1] +=  self.accel
					if e.key == py.K_a:
						self.xyplayer_acl[0] += - self.accel
					if e.key == py.K_d:
						self.xyplayer_acl[0] +=  self.accel
					if e.key == py.K_q:
						self.over = True
				elif e.type == py.KEYUP:
					if e.key == py.K_w:
						self.xyplayer_acl[1] += self.accel
					if e.key == py.K_s:
						self.xyplayer_acl[1] += - self.accel
					if e.key == py.K_a:
						self.xyplayer_acl[0] += self.accel
					if e.key == py.K_d:
						self.xyplayer_acl[0] += - self.accel
				elif e.type == py.MOUSEBUTTONDOWN:
					if e.button == 1:
						self.shooting = True
				elif e.type == py.MOUSEBUTTONUP:
					if e.button == 1:
						self.shooting = False
			py.display.flip()


gs = Gamestate()
