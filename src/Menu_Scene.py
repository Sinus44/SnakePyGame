import pygame
from Button import TextButton

# DELETE ME:
import time

class Menu_Scene:
	def __init__(self, game):
		self.game = game
		
		self.start_button = TextButton(250, 150, "Start Game", self.game.files.fonts["main_font.ttf"])
		self.start_button.on_click = self.start_button_on_click
		self.start_button.on_focus = self.start_button_on_focus
		self.start_button.on_unfocus = self.start_button_on_unfocus

		self.statistic_button = TextButton(250, 200, "Statistic", self.game.files.fonts["main_font.ttf"])
		self.statistic_button.on_click = self.statistic_button_on_click
		self.statistic_button.on_focus = self.statistic_button_on_focus
		self.statistic_button.on_unfocus = self.statistic_button_on_unfocus

		self.quit_button = TextButton(250, 250, "Quit", self.game.files.fonts["main_font.ttf"])
		self.quit_button.on_click = self.quit_button_on_click
		self.quit_button.on_focus = self.quit_button_on_focus
		self.quit_button.on_unfocus = self.quit_button_on_unfocus

		self.title = self.game.files.fonts["main_font.ttf"].render("Snake", True, (255, 255, 255))
		self.creator = self.game.files.fonts["main_font.ttf"].render("Created by Sinus44", True, (255, 255, 255))
		self.fps = 60

		self.updated = True

	def start_button_on_click(self):
		self.game.change_scene("game")
		self.game.files.sounds["click.wav"].play()

	def start_button_on_focus(self):
		self.game.files.sounds["select.wav"].play()
		self.updated = True

	def start_button_on_unfocus(self):
		self.updated = True

	def statistic_button_on_click(self):
		self.game.change_scene("statistic")
		self.game.files.sounds["click.wav"].play()

	def statistic_button_on_focus(self):
		self.game.files.sounds["select.wav"].play()
		self.updated = True

	def statistic_button_on_unfocus(self):
		self.updated = True

	def quit_button_on_click(self):
		self.game.stop()
		self.game.files.sounds["click.wav"].play()

	def quit_button_on_focus(self):
		self.game.files.sounds["select.wav"].play()
		self.updated = True

	def quit_button_on_unfocus(self):
		self.updated = True

	def unselected(self):
		...

	def selected(self):
		self.start_button.focused = False
		self.statistic_button.focused = False
		self.quit_button.focused = False
		self.updated = True

	def tick(self):
		# Обработка ивентов
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.game.stop()
				return

			elif event.type == pygame.KEYDOWN:
				if event.key == 96:
					self.game.change_scene("end")

			elif event.type == pygame.MOUSEMOTION:
				self.start_button.intersection(event.pos)
				self.statistic_button.intersection(event.pos)
				self.quit_button.intersection(event.pos)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.start_button.check_click(event.pos)
				self.statistic_button.check_click(event.pos)
				self.quit_button.check_click(event.pos)

		# Флаг для обновления
		if self.updated:

			# Отрисовка фона
			self.game.screen.blit(self.game.files.images["background.jpg"], (0, 0))
			
			# Отрисовка заголовка
			self.game.screen.blit(self.title, self.title.get_rect(centerx=250, top=0))
			
			# Отрисовка "кем создано"
			self.game.screen.blit(self.creator, self.creator.get_rect(centerx=250, bottom=550))

			# Отрисовка кнопок
			self.start_button.draw(self.game.screen)
			self.statistic_button.draw(self.game.screen)
			self.quit_button.draw(self.game.screen)

			# Обновление экрана
			pygame.display.update()

			# Опускание флага
			self.updated = False
		
		self.game.clock.tick(self.fps)