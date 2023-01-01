import pygame
import os
import math
from Platform import *
from settings import *

class Player():
	def __init__(self, char_type, x, y, scale):
		self.rect = pygame.Rect(x, y, 22 * scale, 40 * scale)
		self.user_text = ''
		self.alive = True
		self.heart = 3
		self.mana = 40
		self.shield = 2
		self.score = 0
		self.dx = 0
		self.dy = 0
		self.go_down = False
		self.angle = 0
		self.scale = scale
		self.vel_y = 0
		self.fire = False
		self.fire_ult = False
		self.run = False
		self.jump = False
		self.flip = False
		self.platform1 = Platform(0, 155, SCREEN_WIDTH, 2)
		self.platform2 = Platform(0, 325, SCREEN_WIDTH, 2)

		self.char_type = char_type
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_clicktime = pygame.time.get_ticks()
		self.update_jumptime = pygame.time.get_ticks()
		self.update_MPtime = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()
		#load all images for player
		animation_types = ['Idle', 'Run', 'Death', 'TakeDamage']
		for animation in animation_types:
			#reset temporary list
			temp_list = []
			#count the file in the folder
			num_of_frames = len(os.listdir(f'Resources/Spritesheets/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'Resources/Spritesheets/{self.char_type}/{animation}/{i}.png')
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]


	def move(self, screen_width, screen_height):
		SPEED = 4
		GRAVITY = 0.75
		self.dx = 0
		self.dy = 0
		self.run = False

		#get keypresses
		key = pygame.key.get_pressed()

		if self.alive:
			#movement
			if key[pygame.K_a] or key[pygame.K_d]:
				self.run = True
				if key[pygame.K_a]:
					self.dx = -SPEED
					self.flip = True
				if key[pygame.K_d]:
					self.dx = SPEED
					self.flip = False

			#go down
			if key[pygame.K_s] and self.go_down == False:
				self.go_down = True
			#jump
			if key[pygame.K_w] and self.jump == False and self.go_down == False:
				if pygame.time.get_ticks() - self.update_jumptime >= 300:
					self.vel_y = -13
					self.jump = True
					self.jump_sound = pygame.mixer.Sound(os.path.join("Resources", "Sound", 'jump.mp3'))
					self.jump_sound.set_volume(0.3)
					pygame.mixer.Sound.play(self.jump_sound)
					self.update_jumptime = pygame.time.get_ticks()
			#increase +2 mp every 1.2 seconds
			if pygame.time.get_ticks() - self.update_MPtime > 1200 and self.mana <= 120:
				self.mana += 1.5
				self.update_MPtime = pygame.time.get_ticks()

		#apply gravity
		if not self.platform1.hits or not self.platform2.hits or self.vel_y != 0:
			self.vel_y += GRAVITY
			self.dy += self.vel_y

		#ensure player stays on screen
		if self.rect.left + self.dx < 0:
			self.dx = -self.rect.left
		if self.rect.right + self.dx > screen_width:
			self.dx = screen_width - self.rect.right
		if self.rect.bottom + self.dy > 490:
			self.vel_y = 0
			self.jump = False
			self.dy = 490 - self.rect.bottom
			self.go_down = False

		#update player position
		self.rect.x += self.dx
		self.rect.y += self.dy

		#check if it's out of range
		if self.heart >= MAX_HEART:
			self.heart = 6
		if self.mana >= MAX_MP:
			self.mana = 150
		if self.shield >= MAX_SHIELD:
			self.shield = 6
		if self.shield <= 0:
			self.shield = 0

		#check if player's hp is less than 0 then player died
		if self.heart <= 0:
			self.alive = False

	def handle_weapon(self, surface):
		player_weapon = pygame.image.load('Resources/Spritesheets/Items/staff.png').convert_alpha()

		#calculate an angle for handling a weapon
		pos = pygame.mouse.get_pos()
		x_dist = pos[0] - self.rect.centerx
		y_dist = -(pos[1] - self.rect.centery)
		weapon_angle = math.degrees(math.atan2(y_dist, x_dist))

		player_weapon_copy = pygame.transform.rotate(player_weapon, weapon_angle)
		surface.blit(player_weapon_copy, (self.rect.centerx - int(player_weapon_copy.get_width() / 2), self.rect.centery + 16 - int(player_weapon_copy.get_height() / 2)))

	def shoot(self, bullet_group):
		#load image
		bullet_img = pygame.image.load('Resources/Spritesheets/Bullet/bullet.png')
		b_w = bullet_img.get_width()
		b_h = bullet_img.get_height()
		bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 2), int(b_h * 2)))

		#define cooldown timer
		SHOOT_COOLDOWN = 400

		#calculate an angle for shooting bullets
		pos = pygame.mouse.get_pos()
		x_dist = pos[0] - self.rect.centerx
		y_dist = -(pos[1] - self.rect.centery)
		self.angle = math.degrees(math.atan2(y_dist, x_dist))
		#get mouseclick
		if pygame.mouse.get_pressed()[0] and self.fire == False and self.mana >= 3:
			if pygame.time.get_ticks() - self.update_clicktime >= SHOOT_COOLDOWN:
				self.fire = True
				self.mana -= 3
				bullet = Bullet(bullet_img, self.rect.centerx, self.rect.centery, self.angle)
				bullet_group.add(bullet)
				self.update_clicktime = pygame.time.get_ticks()
				self.fire_sound = pygame.mixer.Sound(os.path.join("Resources", "Sound", 'fireball.mp3'))
				self.fire_sound.set_volume(0.1)
				pygame.mixer.Sound.play(self.fire_sound)
		if pygame.mouse.get_pressed()[0] == False:
			self.fire = False
			
	def update_animation(self):
		#update what action
		if self.run:
			self.update_action(1)
		elif self.alive == False:
			self.update_action(2)
		else:
			self.update_action(0)

		#update animation
		ANIMATION_COOLDOWN = 100

		#update image on time
		self.image = self.animation_list[self.action][self.frame_index]

		#check the time
		if pygame.time.get_ticks() - self.update_time >= ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#reset frame_index
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.alive == False:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0	

	def update_action(self, new_action):
		#check new action
		if new_action != self.action:
			self.action = new_action
			#reset animation settings
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def show_shield(self, surface, shield, x, y, scale):
		shield_img = pygame.image.load('Resources/Spritesheets/Items/shield.png').convert_alpha()
		shield_w = shield_img.get_width()
		shield_h = shield_img.get_height()
		shield = pygame.transform.scale(shield_img, (int(shield_w * scale), int(shield_h * scale)))
		for i in range(self.shield):
			surface.blit(shield, (x * i + 15, y))

	def draw_heart(self, surface, health, x, y, scale):
		heart_img = pygame.image.load('Resources/Spritesheets/Items/heart.png').convert_alpha()
		heart_w = heart_img.get_width()
		heart_h = heart_img.get_height()
		heart = pygame.transform.scale(heart_img, (int(heart_w * scale), int(heart_h * scale)))
		for i in range(self.heart):
			surface.blit(heart, (x * i + 10, y))

	def draw_MPbar(self, surface, mana, x, y):
		ratio = mana / 150
		pygame.draw.rect(surface, DARK_GRAY, (x, y, 200, 3))
		pygame.draw.rect(surface, BLUE, (x, y, 200 * ratio, 3))

	def draw(self, surface):
		#pygame.draw.rect(surface, WHITE, self.rect)
		surface.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 11, self.rect.y - 2))


class Bullet(pygame.sprite.Sprite):
	def __init__(self, image, x, y, angle):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.angle = math.radians(angle)
		self.speed = 4.4
		#calculate the horizontal and vertical speeds based on the angle
		self.dx = math.cos(self.angle) * self.speed
		self.dy = -(math.sin(self.angle) * self.speed)

	def update(self, surface, screen_width, screen_height):
		#check if bullet has gone out off the screen
		if self.rect.left < 0 or self.rect.right > screen_width or self.rect.bottom < 0 or self.rect.top > screen_height:
			self.kill()
		#move bullet
		self.x = self.x + self.dx
		self.y = self.y + self.dy
		self.rect.centerx = int(self.x)
		self.rect.centery = int(self.y)
		#pygame.draw.rect(surface, (255, 255, 255), self.rect)

class Crosshair():
	def __init__(self, scale):
		image = pygame.image.load('Resources/Spritesheets/Items/crosshair.png').convert_alpha()
		self.scale = scale
		width = image.get_width()
		height = image.get_height()

		self.image = pygame.transform.scale(image, (int(width * self.scale), int(height * self.scale)))
		self.rect = self.image.get_rect()
		pygame.mouse.set_visible(False)

	def draw(self, surface):
		#pygame.draw.rect(surface, BLUE, self.rect)
		mx, my = pygame.mouse.get_pos()
		self.rect.center = (mx, my)
		surface.blit(self.image, (self.rect.x - self.scale, self.rect.y - self.scale))