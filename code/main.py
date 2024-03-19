from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from data import Data
from ui import UI
from button import Button
import pygame, sys
from support import *



class Game:
	def __init__(self, game):
		self.game = game
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Pirate World')
		self.clock = pygame.time.Clock()
		self.import_assets()

		self.ui = UI(self.font, self.ui_frames)
		self.data = Data(self.ui)
		self.tmx_maps = {0: load_pygame(join('data', 'levels', game))}
		self.current_stage = Level(self.tmx_maps[0], self.level_frames, self.data, self.switch_stage)

	def switch_stage(self, target):
		if target == 'death':
			death()
		elif target == 'win':
			win()

	def import_assets(self):
		self.level_frames = {
			'flag': import_folder('graphics', 'level', 'flag'),
			'saw': import_folder('graphics', 'enemies', 'saw', 'animation'),
			'floor_spike': import_folder('graphics', 'enemies', 'floor_spikes'),
			'palms': import_sub_folders('graphics', 'level', 'palms'),
			'candle': import_folder('graphics', 'level', 'candle'),
			'player': import_sub_folders('graphics', 'player'),
			'helicopter': import_folder('graphics', 'level', 'helicopter'),
			'boat': import_folder('graphics', 'objects', 'boat'),
			'items': import_sub_folders('graphics', 'items'),
			'particle': import_folder('graphics', 'effects', 'particle'),
			'water_top': import_folder('graphics', 'level', 'water', 'top'),
			'water_body': import_image('graphics', 'level', 'water', 'body'),
			'bg_tiles': import_folder_dict('graphics', 'level', 'bg', 'tiles'),
			'cloud_small': import_folder('graphics', 'level', 'clouds', 'small'),
			'cloud_large': import_image('graphics', 'level', 'clouds', 'large_cloud')
		}

		self.font = pygame.font.Font(join('graphics', 'ui', 'runescape_uf.ttf'), 40)
		self.ui_frames = {
			'heart': import_folder('graphics', 'ui', 'heart'),
		}

	def run(self):
		while True:
			dt = self.clock.tick(60) / 1000
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
 
			self.current_stage.run(dt)
			self.ui.update(dt)
			pygame.display.update()


pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("graphics/ui/runescape_uf.ttf", size)


def death():
	while True:
		SCREEN.fill("#ddc6a1")

		DEATH_MOUSE_POS = pygame.mouse.get_pos()

		MENU_TEXT = get_font(100).render("You Died", True, "#92a9ce")
		MENU_RECT = MENU_TEXT.get_rect(center=(640, 250))

		PLAY_BACK = Button(image=None, pos=(640, 410), text_input="BACK TO MENU", font=get_font(75), base_color="#92a9ce", hovering_color="#3854b5")

		SCREEN.blit(MENU_TEXT, MENU_RECT)

		for button in [PLAY_BACK]:
			button.changeColor(DEATH_MOUSE_POS)
			button.update(SCREEN)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BACK.checkForInput(DEATH_MOUSE_POS):
					main_menu()

		pygame.display.update()

def win():
	while True:
		SCREEN.fill("#ddc6a1")

		DEATH_MOUSE_POS = pygame.mouse.get_pos()

		MENU_TEXT = get_font(100).render("You Won!", True, "#92a9ce")
		MENU_RECT = MENU_TEXT.get_rect(center=(640, 250))

		PLAY_BACK = Button(image=None, pos=(640, 410), text_input="BACK TO MENU", font=get_font(75), base_color="#92a9ce", hovering_color="#3854b5")

		SCREEN.blit(MENU_TEXT, MENU_RECT)

		for button in [PLAY_BACK]:
			button.changeColor(DEATH_MOUSE_POS)
			button.update(SCREEN)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BACK.checkForInput(DEATH_MOUSE_POS):
					main_menu()

		pygame.display.update()


def play():
	while True:
		PLAY_MOUSE_POS = pygame.mouse.get_pos()

		SCREEN.fill("#ddc6a1")

		PLAY_BACK = Button(image=None, pos=(640, 560), text_input="BACK", font=get_font(75), base_color="#92a9ce", hovering_color="#3854b5")
		PLAY_1 = Button(image=None, pos=(370,360), text_input='Lost At sea', font=get_font(75), base_color="#92a9ce", hovering_color="#3854b5")
		PLAY_2 = Button(image=None, pos=(370,260), text_input='Pirate Bay', font=get_font(75), base_color="#92a9ce", hovering_color="#3854b5")
		PLAY_3 = Button(image=None, pos=(910,260), text_input='The Lab', font=get_font(75), base_color="#92a9ce", hovering_color="#3854b5")
		PLAY_4 = Button(image=None, pos=(910,360), text_input='Candyland', font=get_font(75), base_color="#92a9ce", hovering_color="#3854b5")

		levels = [PLAY_1, PLAY_2, PLAY_3, PLAY_4]

		for button in [PLAY_BACK, PLAY_1, PLAY_2, PLAY_3, PLAY_4]:
			button.changeColor(PLAY_MOUSE_POS)
			button.update(SCREEN)
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
					main_menu()
				for button in levels:
					if button.checkForInput(PLAY_MOUSE_POS):
						if __name__ == '__main__':
							current_level = f'{levels.index(button)}.tmx'
							game = Game(current_level)
							game.run()

		pygame.display.update()

def main_menu():
    while True:
        SCREEN.fill("#ddc6a1")

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#92a9ce")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))

        PLAY_BUTTON = Button(image=None, pos=(640, 350), 
                            text_input="PLAY", font=get_font(75), base_color="#92a9ce", hovering_color="#3854b5")
        QUIT_BUTTON = Button(image=None, pos=(640, 450), 
                            text_input="QUIT", font=get_font(75), base_color="#92a9ce", hovering_color="#3854b5")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
 

