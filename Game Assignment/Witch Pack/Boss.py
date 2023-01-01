import pygame
import os
import math
import random
from Enemies import Items
from settings import *

#define global variables
B1_ATTACK_COOLDOWN = 960
B2_ATTACK_COOLDOWN = 900

class Boss(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, score , mana, scale, damage, direction):
		pygame.sprite.Sprite.__init__(self)
		self.scale = scale
		self.alive = True
		self.vel_y = 0
		self.attack = False
		self.takeDMG = False
		self.flip = direction
		self.score = score
		self.mana = mana
		self.damage = damage
		self.scale = scale

		self.char_type = char_type
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.attack_time = pygame.time.get_ticks()
		self.update_time = pygame.time.get_ticks()
		#load all images for enemies
		animation_types = ['Idle', 'Run', 'Attack', 'Death']
		for animation in animation_types:
			#reset temporary list
			temp_list = []
			#count the file in the folder
			num_of_frames = len(os.listdir(f'Resources/Spritesheets/Boss/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'Resources/Spritesheets/Boss/{self.char_type}/{animation}/{i}.png')
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		if self.char_type == 'Worm':
			self.rect = pygame.Rect(0, 0, 55 * self.scale, 33 * self.scale)
			self.health = boss_health[0]
			self.speed = 2
		if self.char_type == 'Demon':
			self.rect = pygame.Rect(0, 0, 60 * self.scale, 88 * self.scale)
			self.health = boss_health[1]
			self.speed = 2
		self.rect.centerx = x
		self.rect.bottom = y

	def update(self, surface, screen_width, screen_height, target, bullet_group, items_group):
		self.move(surface, screen_width, screen_height, target, bullet_group, items_group)
		self.update_animation()
		self.draw(surface)

	def move(self, surface, screen_width, screen_height, target, bullet_group, items_group):
		GRAVITY = 0.75
		self.dx = 0
		self.dy = 0
		self.attack = False

		if self.alive:
			#check if enemy was hited by bullet
			if pygame.sprite.spritecollide(self, bullet_group, True):
				self.health -= 25

			#ensure enemies face each other
			if self.rect.bottom == target.rect.bottom:
				if target.rect.centerx > self.rect.centerx:
					self.flip = False
					self.dx = self.speed
					if self.rect.right >= target.rect.left and self.rect.bottom == target.rect.bottom and self.action != 4:
						self.attack = True
						self.enemy_attack(surface, target)
					else:
						self.attack = False
				else:
					self.flip = True
					self.dx = - self.speed
					if self.rect.left <= target.rect.right and self.action != 4:
						self.attack = True
						self.enemy_attack(surface, target)
					else:
						self.attack = False
			else:
				if self.rect.x < -80:
					py = random.randint(0, len(enemy_posy) - 1)
					self.flip = False
					self.rect.bottom = enemy_posy[py]
					
				if self.rect.x > SCREEN_WIDTH + 80:
					py = random.randint(0, len(enemy_posy) - 1)
					self.flip = True
					self.rect.bottom = enemy_posy[py]
					
				if self.flip:
					self.dx = - self.speed
				else:
					self.dx = self.speed

			#update enemies position
			if self.action == 1:
				self.rect.x += self.dx
				self.rect.y += self.dy

			#check if enemy's hp goes zero
			if self.health <= 0:
				drop_percentage = random.randint(0, 1)
				if (drop_percentage == 1):
					potion_type = ['hp', 'mp', 'shield']
					r = random.randint(0, 2)
					potion = Items(self.rect.x, self.rect.y, potion_type[r], target)
					items_group.add(potion)
				self.speed = 0
				target.score += self.score
				self.alive = False

	def enemy_attack(self, surface, target):
		if self.flip:
			attacking_rect = pygame.Rect(self.rect.right - 150, self.rect.y, self.rect.width, self.rect.height)
		else:
			attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, self.rect.width, self.rect.height)

		if self.action == 2:
			if self.char_type == 'Worm':
				if self.frame_index == 12:
					if pygame.time.get_ticks() - self.attack_time >= B1_ATTACK_COOLDOWN and target.alive:
						#pygame.draw.rect(surface, (255, 255, 255), attacking_rect)
						if attacking_rect.colliderect(target.rect):
							if target.shield > 0:
								target.shield -= self.damage
							else:
								target.heart -= self.damage
						self.attack_time = pygame.time.get_ticks()
			if self.char_type == 'Demon':
				if self.frame_index == 9:
					if pygame.time.get_ticks() - self.attack_time >= B2_ATTACK_COOLDOWN and target.alive:
						#pygame.draw.rect(surface, (255, 255, 255), attacking_rect)
						if attacking_rect.colliderect(target.rect):
							if target.shield > 0:
								target.shield -= self.damage
							else:
								target.heart -= self.damage
						self.attack_time = pygame.time.get_ticks()

		if target.alive == False:
			self.update_action(0)

	def update_animation(self):
		#update what action
		if self.attack:
			self.update_action(2)
		elif self.alive == False:
			self.update_action(3)
		else:
			self.update_action(1)

		#update animation
		ANIMATION_COOLDOWN = 60

		#update image on time
		self.image = self.animation_list[self.action][self.frame_index]

		#check the time
		if pygame.time.get_ticks() - self.update_time >= ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#reset frame_index
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
				self.kill()
			elif self.action == 4:
				self.takeDMG = False
				self.frame_index = 0
			else:
				self.frame_index = 0	

	def update_action(self, new_action):
		#check new action
		if new_action != self.action:
			self.action = new_action
			#reset animation settings
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()

	def draw(self, surface):
		#pygame.draw.rect(surface, (255, 255, 255), self.rect)
		if self.char_type == 'Worm':
			surface.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 35, self.rect.y - 50))
		if self.char_type == 'Demon':
			surface.blit(pygame.transform.flip(self.image, not self.flip, False), (self.rect.x - 135, self.rect.y - 70))