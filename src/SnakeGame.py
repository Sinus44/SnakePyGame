from Files import Files
from Menu_Scene import Menu_Scene
from Game_Scene import Game_Scene
from End_Scene import End_Scene
from Statistic_Scene import Statistic_Scene
import pygame

class SnakeGame:
	def __init__(self):
		# Переменные
		self.W = 500
		self.H = 550

		self.last_game_score = None
		self.last_game_win = None
		self.selected_scene = None
		self.screen = None
		self.clock = pygame.time.Clock()

		# Файлы игры
		self.files = Files()
		self.files.load_images()
		self.files.load_sounds()
		self.files.load_fonts(36)

		# Сцены
		self.menu_scene = Menu_Scene(self)
		self.game_scene = Game_Scene(self)
		self.end_scene = End_Scene(self)
		self.statistic_scene = Statistic_Scene(self)

		# Выбор начальной сцены
		self.change_scene("menu")

	def stop(self):
		self.enable = False

	def change_scene(self, new_scene):
		changed = True
		old_scene = self.selected_scene
		if new_scene == "game":
			self.selected_scene = self.game_scene

		elif new_scene == "menu":
			self.selected_scene = self.menu_scene

		elif new_scene == "end":
			self.selected_scene = self.end_scene

		elif new_scene == "statistic":
			self.selected_scene = self.statistic_scene

		else:
			changed = False

		if changed:
			if old_scene: old_scene.unselected()
			self.selected_scene.selected()

	def start(self):
		if not self.selected_scene:
			return

		self.screen = pygame.display.set_mode((self.W, self.H))
		pygame.display.set_caption("Snake v0.2b")
		pygame.display.set_icon(self.files.images["icon.png"])
		
		self.enable = True

		while self.enable:
			self.selected_scene.tick()

# FIXME: Удалить это при релизе
if __name__ == "__main__":
	snake_game = SnakeGame()
	snake_game.start()