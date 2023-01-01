import pygame

#game settings
TITLE = "Witch Fight!"

#screen setting
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#fps setting
FPS = 60

#define color
BG = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 255, 255)

#define player max stat values
MAX_HEART = 6
MAX_MP = 150
MAX_SHIELD = 6

#about enemies
enemy_type = ['Goblin', 'Skeleton', 'Mushroom', 'Flying eye']
enemy_health = [25, 50, 75, 50]
enemy_posx = [-50, SCREEN_WIDTH + 50]
enemy_posy = [490, 325, 155]
enemy_scale = [1, 1, 1.4, 1.5]
enemy_gavescore = [5, 10, 15, 10]
enemy_damage = [1, 1, 2, 1]
enemy_gavemp = [2, 3, 5, 3]
enemy_dir = [True, False]

boss_health = [105, 168]
boss_gavescore = [75, 150]
boss_damage = [4, 6]
boss_gavemp = [30, 60]
boss_scale = [1, 2]