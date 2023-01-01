import pygame
import random
import os
import sys
import json
from settings import *
from Menu import *
from Player import *
from Enemies import *
from Boss import *
from Platform import *
from Leaderboard import *

class Game():
	def __init__(self):
		pygame.init()
		self.running, self.playing, self.naming, self.is_over = True, False, False, False
		self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.PAUSE = False, False, False, False, False
		self.DISPLAY_W, self.DISPLAY_H = SCREEN_WIDTH, SCREEN_HEIGHT
		self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
		self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
		pygame.display.set_caption('Witch Packs!')
		self.font_name = os.path.join("Resources", "Font", '8-BIT WONDER.TTF')
		self.font_name1 = pygame.font.SysFont("arial.ttf", 22)
		self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
		self.main_menu = MainMenu(self)
		self.leaderboard_menu = LeaderboardMenu(self)
		self.pause_menu = PauseMenu(self)
		self.curr_menu = self.main_menu
		self.state = 'Mainmenu'

		#load background
		self.board_bg = pygame.image.load('Resources/Spritesheets/Map/gray.jpg')
		self.bg_image = pygame.image.load('Resources/Spritesheets/Map/forest.png')
		self.bg_clouds = pygame.image.load('Resources/Spritesheets/Map/clouds.png')
		self.clouds_rect = self.bg_clouds.get_rect()
		#set clock
		self.clock = pygame.time.Clock()
		#create groups
		self.platform_group = pygame.sprite.Group()
		self.bullet_group = pygame.sprite.Group()
		self.enemy_group = pygame.sprite.Group()
		self.boss_group = pygame.sprite.Group()
		self.items_group = pygame.sprite.Group()
		#create platforms
		self.platform_img = pygame.image.load('Resources/Spritesheets/Map/platform.png')
		self.platform1 = Platform(0, 155, SCREEN_WIDTH, 2)
		self.platform2 = Platform(0, 325, SCREEN_WIDTH, 2)
		#create crosshair
		self.crosshair = Crosshair(1.25)
		#create an instance of player
		self.player = Player('Player', 350, 470, 2)

		self.level = 1
		self.level_difficulty = 0
		self.target_difficulty = 300
		self.level_timer = pygame.time.get_ticks()
		self.level_reset_timer = pygame.time.get_ticks()
		self.DIFFICULTY_MULTIPLIER = 1.3
		self.next_level = False
		self.game_over = False

		self.ENEMY_TIMER = 1200
		self.last_enemy = pygame.time.get_ticks()
		self.enemies_alive = 0
		self.bosses_alive = 0


	def game_loop(self):
		while self.playing:
			if self.game_over == False and self.PAUSE == False:
				self.clock.tick(FPS)
				self.check_events()
				self.display.fill(self.BLACK)
				self.draw_bg()

				#draw player
				self.player.update_animation()
				self.player.move(self.DISPLAY_W, self.DISPLAY_H)
				self.player.draw(self.display)
				#draw weapon
				if self.player.alive:
					self.player.handle_weapon(self.display)
					self.player.shoot(self.bullet_group)
				#player.ultimate_shoot(screen)
				self.player.draw_heart(self.display, self.player.heart, 25, 5, 2.5)
				self.player.show_shield(self.display, self.player.shield, 25, 35, 0.9)
				self.player.draw_MPbar(self.display, self.player.mana, 20, 67)

				#draw platforms
				self.platform1.update(self.display, self.player)
				self.platform2.update(self.display, self.player)
				
				#draw bosses
				self.boss_group.update(self.display, self.DISPLAY_H, self.DISPLAY_W, self.player, self.bullet_group, self.items_group)
				#draw enemies
				self.enemy_group.update(self.display, self.DISPLAY_H, self.DISPLAY_W, self.player, self.bullet_group, self.items_group)
				#create enemies
				#check if the max number of enemies has been reached
				if self.level_difficulty < self.target_difficulty:
					if pygame.time.get_ticks() - self.last_enemy >= self.ENEMY_TIMER:
						if self.level % 3 == 0:
							px = random.randint(0, len(enemy_posx) - 1)
							py = random.randint(0, len(enemy_posy) - 1)
							if px == 0:
								d = 1
							else:
								d = 0
							self.boss = Boss('Worm', enemy_posx[px], enemy_posy[py], boss_gavescore[0], boss_gavemp[0], boss_scale[1], boss_damage[0], enemy_dir[d])
							self.boss.health *= 1.19
							self.boss_group.add(self.boss)
							self.level_difficulty = self.target_difficulty
						elif self.level % 5 == 0:
							px = random.randint(0, len(enemy_posx) - 1)
							py = random.randint(0, len(enemy_posy) - 1)
							self.boss = Boss('Demon', enemy_posx[px], enemy_posy[py], boss_gavescore[1], boss_gavemp[1], boss_scale[0], boss_damage[1], enemy_dir[px])
							self.boss.health *= 1.19
							self.boss_group.add(self.boss)
							self.level_difficulty = self.target_difficulty
						else:
							e = random.randint(0, len(enemy_type) - 1)
							px = random.randint(0, len(enemy_posx) - 1)
							if px == 0:
								d = 1
							else:
								d = 0
							if e == 3:
								py = random.randint(1, len(enemy_posy) - 1)
							else:
								py = random.randint(0, len(enemy_posy) - 1)
							self.enemy = Enemy(enemy_type[e], enemy_health[e], enemy_posx[px], enemy_posy[py], enemy_scale[e], enemy_gavescore[e], enemy_damage[e], enemy_dir[px])
							self.enemy_group.add(self.enemy)
							self.last_enemy = pygame.time.get_ticks()
							self.level_difficulty += enemy_health[e]

				#check if all the enemies have been spawned
				if self.level_difficulty >= self.target_difficulty:
					#check how many enemies alive
					self.enemies_alive = 0
					for e in self.enemy_group:
						if e.alive == True:
							self.enemies_alive += 1
					self.bosses_alive = 0
					for b in self.boss_group:
						if b.alive == True:
							self.bosses_alive += 1
					#if all the enemies are dead
					if self.enemies_alive == 0 and self.bosses_alive == 0 and self.next_level == False:
						self.next_level = True
						self.level_timer = pygame.time.get_ticks()
							
					#move on to the next level
				if self.next_level == True:
					if pygame.time.get_ticks() - self.level_timer > 3000:
						self.boss_group.empty()
						self.enemy_group.empty()
						self.items_group.empty()
					self.next_level = False
					self.level += 1
					self.last_enemy = pygame.time.get_ticks()
					self.target_difficulty *= self.DIFFICULTY_MULTIPLIER
					self.level_difficulty = 0

				#draw props
				self.draw_props()

				#draw items
				self.items_group.update(self.display, self.player)

				#draw crosshair
				self.crosshair.draw(self.display)

				#draw bullet
				self.bullet_group.update(self.display, self.DISPLAY_W, self.DISPLAY_H)
				self.bullet_group.draw(self.display)

				#draw wave and time
				self.draw_text('WAVE ' + str(self.level), 20, 380, 20)
				self.draw_text('SCORE ' + str(self.player.score), 20, 680, 20)
				self.draw_text4("Made by", 790, 560)
				self.draw_text4("Thanathat Pinthu (65010409)", 790, 580)
				self.draw_text3("Use WASD keys to control the player", 10, 540)
				self.draw_text3("Use Mouse to control crosshair", 10, 560)
				self.draw_text3("Click left to fire a bullet", 10, 580)

				if self.player.alive == False:
					self.game_over = True
				if self.PAUSE:
					self.curr_menu = self.pause_menu
					self.playing = False
					self.curr_menu.run_display = True

			else:
				if self.is_over == False:
					self.check_events()
					self.display.fill(self.BLACK)
					self.draw_bg2()
					self.draw_text('GAME OVER', 30, self.DISPLAY_W / 2, self.DISPLAY_H / 2 - 50)
					self.draw_text('YOU DIED', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
					self.draw_text('YOUR SCORE ' + str(self.player.score), 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2 + 50)
					if self.START_KEY:
						self.naming = True
						while self.naming:
							self.display.fill(self.BLACK)
							self.draw_bg2()
							self.draw_text("Input your name :", 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2 - 40)
							self.draw_text4("Made by", 790, 560)
							self.draw_text4("Thanathat Pinthu (65010409)", 790, 580)
							for event in pygame.event.get():
								if event.type == pygame.KEYDOWN:
									if event.key == pygame.K_RETURN:
										self.naming = False
										self.is_over = True
									elif event.key == pygame.K_BACKSPACE:
										self.player.user_text = self.player.user_text[:-1]
									else:
										self.player.user_text += event.unicode
							self.draw_text(self.player.user_text, 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
							self.window.blit(self.display, (0, 0))
							pygame.display.update()
						leaderboard = Leaderboard(self.player.user_text, self.player.score)
						leaderboard.load_previous_scores()
						leaderboard.save_score()
						self.reset_keys()
				if self.is_over:
					self.check_events()
					self.display.fill(self.BLACK)
					self.draw_bg2()
					self.draw_text("Leaderboard", 30, self.DISPLAY_W / 2, self.DISPLAY_H / 2 - 240)
					self.draw_board()
					self.draw_text('*', 15, self.DISPLAY_W / 2 - 100, self.DISPLAY_H / 2 + 250)
					self.draw_text("MainMenu", 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2 + 250)
					self.draw_text4("Made by", 790, 560)
					self.draw_text4("Thanathat Pinthu (65010409)", 790, 580)
					if self.START_KEY:
						if self.state == 'Mainmenu':
							self.curr_menu = self.main_menu
						self.playing = False
			self.window.blit(self.display, (0, 0))
			pygame.display.update()
			self.reset_keys()

	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running, self.playing = False, False
				self.curr_menu.run_display = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					self.START_KEY = True
				if event.key == pygame.K_BACKSPACE:
					self.BACK_KEY = True
				if event.key == pygame.K_w:
					self.UP_KEY = True
				if event.key == pygame.K_s:
					self.DOWN_KEY = True
				if event.key == pygame.K_x:
					self.PAUSE = True

	def reset_keys(self):
		self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.PAUSE = False, False, False, False, False

	def reset_game(self):
		self.boss_group.empty()
		self.enemy_group.empty()
		self.user_text = ''
		self.player = Player('Player', 350, 470, 2)
		self.level = 1
		self.level_difficulty = 0
		self.target_difficulty = 300
		self.level_reset_timer = pygame.time.get_ticks()
		self.DIFFICULTY_MULTIPLIER = 1.5
		self.next_level = False
		self.game_over = False
		self.is_over = False
		self.ENEMY_TIMER = 1200
		self.last_enemy = pygame.time.get_ticks()
		self.enemies_alive = 0

	def draw_text(self, text, size, x, y):
		font = pygame.font.Font(self.font_name, size)
		text_surface = font.render(text, True, self.WHITE)
		text_rect = text_surface.get_rect()
		text_rect.center = (x, y)
		self.display.blit(text_surface, text_rect)

	def draw_text2(self, text, size, x, y):
		font2 = pygame.font.Font(self.font_name, size)
		text_surface2 = font2.render(text, True, self.WHITE)
		text_rect2 = text_surface2.get_rect()
		text_rect2.x = x
		text_rect2.y = y
		self.display.blit(text_surface2, text_rect2)

	def draw_text3(self, text, x, y):
		font3 = self.font_name1
		text_surface3 = font3.render(text, True, self.WHITE)
		text_rect3 = text_surface3.get_rect()
		text_rect3.x = x
		text_rect3.y = y
		self.display.blit(text_surface3, text_rect3)

	def draw_text4(self, text, x, y):
		font4 = self.font_name1
		text_surface4 = font4.render(text, True, self.WHITE)
		text_rect4 = text_surface4.get_rect()
		text_rect4.right = x
		text_rect4.y = y
		self.display.blit(text_surface4, text_rect4)

	def draw_bg(self):
		scaled_bg = pygame.transform.scale(self.bg_image, (self.DISPLAY_W, self.DISPLAY_H))
		scaled_clouds = pygame.transform.scale(self.bg_clouds, (self.DISPLAY_W, 80))
		scaled_platform = pygame.transform.scale(self.platform_img, (self.DISPLAY_W, 13))
		self.display.blit(scaled_bg, (0, -70))
		self.display.blit(pygame.transform.flip(scaled_clouds, True, False), (0, 0))
		self.display.blit(scaled_platform, (0, 155))
		self.display.blit(scaled_platform, (0, 325))

	def draw_bg2(self):
		scaled_bg = pygame.transform.scale(self.board_bg, (self.DISPLAY_W, self.DISPLAY_H))
		self.display.blit(scaled_bg, (0, 0))

	def draw_image(self, image, x, y, scale):
		img = pygame.image.load(f'Resources/Spritesheets/Map/{image}.png')
		img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
		self.display.blit(img, (x, y))

	def draw_props(self):
		self.draw_image('bush1', 340, 475, 3)
		self.draw_image('mush3', 420, 500, 2)
		self.draw_image('rock4', 210, 510, 2.2)
		self.draw_image('bush1', 230, 500, 3)
		self.draw_image('bush2', 110, 510, 3)
		self.draw_image('bush3', 65, 510, 2)
		self.draw_image('Tree1', -70, 460, 0.9)
		self.draw_image('rock1', -100, 480, 1.6)
		self.draw_image('rock1', 600, 480, 1.6)
		self.draw_image('rock4', 430, 550, 2.2)
		self.draw_image('mush2', 230, 490, 2)
		self.draw_image('rock3', 120, 550, 2.2)
		self.draw_image('mush2', 550, 490, 2)
		self.draw_image('Tree1', 560, 460, 0.9)
		self.draw_image('rock3', 500, 550, 2.2)
		self.draw_image('bush3', 700, 550, 2)
		self.draw_image('mush1', 620, 550, 2)
		self.draw_image('mush1', 10, 540, 2)

	def draw_board(self):
		padding_y = 0
		max_scores = 10 # We *could* paint every score, but it's not any good if you can't see them (because we run out of the screen).
		nbr_scores = 1
		with open("highscore.json", 'r') as highscore_file:
			self.scores = json.loads(highscore_file.read())
			self.scores = self.scores
		for score in self.scores:
			if nbr_scores <= max_scores:
				self.draw_text2(str(nbr_scores)+") " +str(score["name"]), 20, 240, 120 + padding_y)
				self.draw_text2(str(score["score"]), 20, 490, 120 + padding_y)
				padding_y += 40
				nbr_scores += 1