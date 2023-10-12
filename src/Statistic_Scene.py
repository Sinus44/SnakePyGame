import pygame
from Button import TextButton
from Records import Records

class Statistic_Scene:
	def __init__(self, game):
		self.game = game

		self.title = self.game.files.fonts["main_font.ttf"].render("Records", True, (255, 255, 255))
		
		self.menu_button = TextButton(50, 30, "MENU", self.game.files.fonts["main_font.ttf"])
		self.menu_button.on_click = lambda: self.game.change_scene("menu") or self.game.files.sounds["click.wav"].play()
		self.menu_button.on_focus = self.menu_button_on_focus
		self.menu_button.on_unfocus = self.menu_button_on_unfocus

		self.fps = 60
		self.updated = True

	def menu_button_on_focus(self):
		self.game.files.sounds["select.wav"].play()
		self.updated = True

	def menu_button_on_unfocus(self):
		self.updated = True

	def unselected(self): 
		...

	def selected(self):
		self.records = Records.load()
		self.records = dict(sorted(self.records.items(), key=lambda item: item[1], reverse=True))
		self.scores = [self.game.files.fonts["main_font.ttf"].render(f"{name}: {self.records[name]}", True, (255, 255, 255)) for name in self.records][:5]
		self.menu_button.focused = False
		self.updated = True

	def tick(self):
		# Обработка ивентов
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.game.stop()
				return

			elif event.type == pygame.MOUSEMOTION:
				self.menu_button.intersection(event.pos)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.menu_button.check_click(event.pos)

		if self.updated:
			# Отрисовка фона
			self.game.screen.blit(self.game.files.images["background.jpg"], (0, 0))
			
			# Отрисовка заголовка
			self.game.screen.blit(self.title, self.title.get_rect(center=(250, 50)))

			# Отрисовка заголовка
			for i, record in enumerate(self.scores):
				self.game.screen.blit(record, record.get_rect(center=(250, 150 + 50 * i)))

			# Отрисовка кнопки "в меню"
			self.menu_button.draw(self.game.screen)

			# Обновление экрана
			pygame.display.update()

			# Опускание флага
			self.updated = False

		self.game.clock.tick(self.fps)
