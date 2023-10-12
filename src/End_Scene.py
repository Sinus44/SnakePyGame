import pygame
from Button import TextButton
from Inputbox import Inputbox
from Records import Records

class End_Scene:
	def __init__(self, game):
		self.game = game

		self.nickname_title = self.game.files.fonts["main_font.ttf"].render("NICKNAME:", True, (255, 255, 255))

		self.name_inputbox = Inputbox(150, 230, 200, 50, self.game.files.fonts["main_font.ttf"], "PLAYER", 8)

		self.save_button = TextButton(250, 300, "SAVE", self.game.files.fonts["main_font.ttf"])
		self.save_button.on_click = self.save_result
		self.save_button.on_focus = lambda: self.game.files.sounds["select.wav"].play()

		self.win_title = self.game.files.fonts["main_font.ttf"].render("You Win", True, (255, 255, 255))
		self.lose_title = self.game.files.fonts["main_font.ttf"].render("You Lose", True, (255, 255, 255))

		self.title = None

		self.fps = 30

	def unselected(self):
		...

	def save_result(self):
		self.game.files.sounds["click.wav"].play()
		Records.load()
		Records.set(self.name_inputbox.text, self.game.last_game_score)
		Records.save()
		self.game.change_scene("menu")

	def selected(self):
		self.save_button.focused = False
		self.name_inputbox.selected = False
		self.score = self.game.files.fonts["main_font.ttf"].render(f"Score: {self.game.last_game_score}", True, (255, 255, 255))
		self.title = self.win_title if self.game.last_game_win else self.lose_title

	def tick(self):
		# Обработка ивентов
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.game.stop()
				return

			elif event.type == pygame.TEXTINPUT:
				self.name_inputbox.input(event.text)

			elif event.type == pygame.KEYDOWN:
				if event.key == 8:
					self.name_inputbox.input("", True)

			elif event.type == pygame.MOUSEMOTION:
				self.save_button.intersection(event.pos)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.save_button.check_click(event.pos)
				self.name_inputbox.intersection(event.pos)

		# Отрисовка фона
		self.game.screen.blit(self.game.files.images["background.jpg"], (0, 0))
		
		# Отрисовка заголовка
		self.game.screen.blit(self.title, self.title.get_rect(center=(250, 50)))

		# Отрисовка лейбла для ника
		self.game.screen.blit(self.nickname_title, self.nickname_title.get_rect(center=(250, 200)))

		# Отрисовка заголовка
		self.game.screen.blit(self.score, self.score.get_rect(center=(250, 100)))

		self.name_inputbox.draw(self.game.screen)

		#self.menu_button.draw(self.game.screen)
		self.save_button.draw(self.game.screen)

		pygame.display.flip()
		self.game.clock.tick(self.fps)