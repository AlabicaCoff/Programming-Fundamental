import pygame
import os
import json

class Menu():
	def __init__(self, game):
		self.game = game
		self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
		self.run_display = True
		self.cursor_rect = pygame.Rect(0, 0, 20, 20)
		self.offset = - 120
		self.frame_index = 0
		self.bg_image1 = pygame.image.load('Resources/Spritesheets/Map/cover.jpg')
		self.bg_image2 = pygame.image.load('Resources/Spritesheets/Map/gray.jpg')
		self.temp_list = []
		#count the file in the folder
		num_of_frames = len(os.listdir(f'Resources/Spritesheets/Player/Idle'))
		for i in range(num_of_frames):
			img = pygame.image.load(f'Resources/Spritesheets/Player/Idle/{i}.png')
			img = pygame.transform.scale(img, (int(img.get_width() * 5), int(img.get_height() * 5)))
			self.temp_list.append(img)
		self.image = self.temp_list[self.frame_index]
		self.rect = self.image.get_rect()
		self.update_time = pygame.time.get_ticks()
		pygame.mixer.music.load(os.path.join("Resources", "Sound", 'music.wav'))
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play(-1)
		pygame.mouse.set_visible(True)

	def update_animation(self):
		#update animation
		ANIMATION_COOLDOWN = 150

		#update image on time
		self.image = self.temp_list[self.frame_index]

		#check the time
		if pygame.time.get_ticks() - self.update_time >= ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#reset frame_index
		if self.frame_index >= len(self.temp_list):
			self.frame_index = 0	

	def draw_cursor(self):
		self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

	def blit_screen(self):
		self.game.window.blit(self.game.display, (0, 0))
		self.update_animation()
		pygame.display.update()
		self.game.reset_keys()

class MainMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = 'Start'
		self.startx, self.starty = self.mid_w / 1.5, self.mid_h + 95
		self.leaderboardx, self.leaderboardy = self.mid_w / 1.5, self.mid_h + 135
		self.exitx, self.exity = self.mid_w / 1.5, self.mid_h + 175
		self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
		pygame.mouse.set_visible(True)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.draw_bg()
			self.game.draw_text('Main Menu', 30, self.game.DISPLAY_W / 3, self.game.DISPLAY_H / 2 + 45 )
			self.game.draw_text("New Game", 20, self.startx, self.starty)
			self.game.draw_text("Leaderboard", 20, self.leaderboardx, self.leaderboardy)
			self.game.draw_text("Exit Game", 20, self.exitx, self.exity)
			self.game.draw_text3("Use W and S keys to navigate", 10, 560)
			self.game.draw_text3("Enter to select", 10, 580)
			self.game.draw_text4("Made by", 790, 560)
			self.game.draw_text4("Thanathat Pinthu (65010409)", 790, 580)
			self.draw_cursor()
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'Start':
				self.cursor_rect.midtop = (self.leaderboardx + self.offset, self.leaderboardy)
				self.state = 'Leaderboard'
			elif self.state == 'Leaderboard':
				self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
				self.state = 'Exit'
			elif self.state == 'Exit':
				self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
				self.state = 'Start'

		elif self.game.UP_KEY:
			if self.state == 'Start':
				self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
				self.state = 'Exit'
			elif self.state == 'Leaderboard':
				self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
				self.state = 'Start'
			elif self.state == 'Exit':
				self.cursor_rect.midtop = (self.leaderboardx + self.offset, self.leaderboardy)
				self.state = 'Leaderboard'

	def check_input(self):
		self.move_cursor()
		if self.game.START_KEY:
			if self.state == 'Start':
				pygame.mixer.music.fadeout(500)
				self.game.reset_game()
				self.game.playing = True
			elif self.state == 'Leaderboard':
				self.game.curr_menu = self.game.leaderboard_menu
			elif self.state == 'Exit':
				self.game.running = False
			self.run_display = False

	def draw_bg(self):
		player_weapon = pygame.image.load('Resources/Spritesheets/Items/staff.png').convert_alpha()
		player_weapon_copy = pygame.transform.rotate(player_weapon, 90)
		scaled_weapon = pygame.transform.scale(player_weapon_copy, (int(player_weapon_copy.get_width() * 2), int(player_weapon_copy.get_height() * 2)))
		scaled_bg = pygame.transform.scale(self.bg_image1, (self.game.DISPLAY_W, self.game.DISPLAY_H))
		self.game.display.blit(scaled_bg, (0, 0))
		self.game.display.blit(pygame.transform.flip(self.image, True, False), (500, 285))
		self.game.display.blit(scaled_weapon, (540, 365))
		pygame.display.update()

class LeaderboardMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = 'Mainmenu'
		self.leaderboardx, self.leaderboardy = self.mid_w, self.mid_h - 240
		self.mainmenux, self.mainmenuy = self.mid_w, self.mid_h + 250
		self.offset = - 90
		self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
		pygame.mouse.set_visible(True)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill((0, 0, 0))
			self.draw_bg()
			self.game.draw_text("Leaderboard", 30, self.leaderboardx, self.leaderboardy)
			self.draw_board()
			self.game.draw_text("MainMenu", 20, self.mainmenux, self.mainmenuy)
			self.game.draw_text3("Enter to select", 10, 580)
			self.game.draw_text4("Made by", 790, 560)
			self.game.draw_text4("Thanathat Pinthu (65010409)", 790, 580)
			self.draw_cursor()
			self.blit_screen()

	def check_input(self):
		if self.game.START_KEY:
			if self.state == 'Mainmenu':
				self.game.curr_menu = self.game.main_menu
			self.run_display = False

	def draw_board(self):
		padding_y = 0
		max_scores = 10 # We *could* paint every score, but it's not any good if you can't see them (because we run out of the screen).
		nbr_scores = 1
		with open("highscore.json", 'r') as highscore_file:
			self.scores = json.loads(highscore_file.read())
			self.scores = self.scores
		for score in self.scores:
			if nbr_scores <= max_scores:
				self.game.draw_text2(str(nbr_scores)+") " +str(score["name"]), 20, 240, 120 + padding_y)
				self.game.draw_text2(str(score["score"]), 20, 490, 120 + padding_y)
				padding_y += 40
				nbr_scores += 1

	def draw_bg(self):
		scaled_bg = pygame.transform.scale(self.bg_image2, (self.game.DISPLAY_W, self.game.DISPLAY_H))
		self.game.display.blit(scaled_bg, (0, 0))
		pygame.display.update()
	
class PauseMenu(Menu):
	def __init__(self, game):
		Menu.__init__(self, game)
		self.state = 'Play'
		self.playx, self.playy = self.mid_w, self.mid_h + 30
		self.mainmenux, self.mainmenuy = self.mid_w, self.mid_h + 60
		self.cursor_rect.midtop = (self.playx + self.offset, self.playy)
		pygame.mouse.set_visible(True)

	def display_menu(self):
		self.run_display = True
		while self.run_display:
			self.game.check_events()
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.draw_bg()
			self.game.draw_text('PAUSE', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
			self.game.draw_text("Play", 20, self.playx, self.playy)
			self.game.draw_text("Mainmenu", 20, self.mainmenux, self.mainmenuy)
			self.game.draw_text3("Use W and S keys to navigate", 10, 560)
			self.game.draw_text3("Enter to select", 10, 580)
			self.game.draw_text4("Made by", 790, 560)
			self.game.draw_text4("Thanathat Pinthu (65010409)", 790, 580)
			self.draw_cursor()
			self.blit_screen()

	def move_cursor(self):
		if self.game.DOWN_KEY:
			if self.state == 'Play':
				self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
				self.state = 'Mainmenu'
			elif self.state == 'Mainmenu':
				self.cursor_rect.midtop = (self.playx + self.offset, self.playy)
				self.state = 'Play'

		elif self.game.UP_KEY:
			if self.state == 'Play':
				self.cursor_rect.midtop = (self.mainmenux + self.offset, self.mainmenuy)
				self.state = 'Mainmenu'
			elif self.state == 'Mainmenu':
				self.cursor_rect.midtop = (self.playx + self.offset, self.playy)
				self.state = 'Play'

	def check_input(self):
		self.move_cursor()
		if self.game.START_KEY:
			if self.state == 'Play':
				self.game.PAUSE = False
				self.game.playing = True
			elif self.state == 'Mainmenu':
				self.game.curr_menu = self.game.main_menu
				pygame.mixer.music.load(os.path.join("Resources", "Sound", 'music.wav'))
				pygame.mixer.music.set_volume(0.5)
				pygame.mixer.music.play(-1)
			self.run_display = False

	def draw_bg(self):
		scaled_bg = pygame.transform.scale(self.bg_image2, (self.game.DISPLAY_W, self.game.DISPLAY_H))
		self.game.display.blit(scaled_bg, (0, 0))
		pygame.display.update()