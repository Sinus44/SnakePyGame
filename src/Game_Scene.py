import pygame
from Button import ImageButton
import time
import random

class Game_Scene:
	def __init__(self, game):
		self.game = game
		
		self.fps = 0
		#self.cell_size = 30

		self.menu_button = ImageButton(250, 25, pygame.transform.scale(self.game.files.images["icon.png"], (50, 50)))
		self.menu_button.on_click = self.menu_button_on_click
		self.menu_button.on_focus = self.menu_button_on_focus
		self.menu_button.on_unfocus = self.menu_button_on_unfocus

		self.snake = None
		self.snake_directions = None
		self.timer = None
		self.fast = None
		self.score = None
		self.score_text = None

		self.updated = True

		self.update_score_text()

	def menu_button_on_click(self):
		self.game.change_scene("menu") or self.game.files.sounds["click.wav"].play()

	def menu_button_on_focus(self):
		self.game.files.sounds["select.wav"].play()
		self.updated = True

	def menu_button_on_unfocus(self):
		self.updated = True

	def update_score_text(self):
		self.score_text = self.game.files.fonts["main_font.ttf"].render(f"Score: {self.score or 0}", True, (255, 255, 255))

	def selected(self):
		self.snake = [(9, 9)]
		self.snake_directions = [0]
		self.direction = [0, 0]
		self.new_direction = [0, 0]
		self.apple = [0, 0]
		self.score = 0
		self.update_score_text()

		self.fast = False
		self.menu_button.focused = False
		self.timer = time.time()
		self.updated = True

		# Генерируем позицию яблока
		self.generate_apple_pos()

		# Включаем музыку
		pygame.mixer.music.play(-1)

		# Выключаем курсор
		pygame.mouse.set_visible(False)

	def unselected(self):
		# Выключение музыки
		pygame.mixer.music.stop()

		# Включаем курсор
		pygame.mouse.set_visible(True) 

	def generate_apple_pos(self):
		new_pos = [random.randint(0, 19), random.randint(0, 19)]

		while new_pos in self.snake:
			new_pos = [random.randint(0, 19), random.randint(0, 19)]

		self.apple = new_pos

	def angle_from_dir(self, direction):
		if direction == [1, 0]:
			return 0
		elif direction == [-1, 0]:
			return 180

		elif direction == [0, 1]:
			return 270

		elif direction == [0, -1]:
			return 90

		return 0

	def move(self):
		self.timer = time.time()
		self.direction = self.new_direction
		new_pos = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]

		# Коллизия со змейкой и стеной
		if (new_pos in self.snake) and (self.direction != [0, 0]) or \
				(19 < new_pos[0]) or (new_pos[0] < 0) or (19 < new_pos[1]) or (new_pos[1] < 0):

			self.game.files.sounds["bonk.wav"].play()
			self.game.last_game_win = False
			self.game.last_game_score = self.score
			self.game.change_scene("end")

		self.snake.insert(0, new_pos)
		self.snake_directions.insert(0, self.direction)

		if new_pos == self.apple:
			self.game.files.sounds["apple.wav"].play()
			self.score += 1
			self.update_score_text()
			self.generate_apple_pos()
		else:
			self.snake.pop(-1)
			self.snake_directions.pop(-1)

		if len(self.snake) == 400:
			self.game.last_game_win = True
			self.game.last_game_score = self.score
			self.game.files.sounds["win.wav"].play()
			self.game.change_scene("end")

		self.updated = True

	def tick(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.game.stop()
				return

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w or event.key == pygame.K_UP: # W
					if self.direction == [0, -1]:
						self.fast = True

					if self.direction != [0, 1]:
						self.new_direction = [0, -1]
						self.move()

				elif event.key == pygame.K_s or event.key == pygame.K_DOWN: # S
					if self.direction == [0, 1]:
						self.fast = True

					if self.direction != [0, -1]:
						self.new_direction = [0, 1]
						self.move()

				elif event.key == pygame.K_a or event.key == pygame.K_LEFT: # A
					if self.direction == [-1, 0]:
						self.fast = True

					if self.direction != [1, 0]:
						self.new_direction = [-1, 0]
						self.move()
					
				elif event.key == pygame.K_d or event.key == pygame.K_RIGHT: # D
					if self.direction == [1, 0]:
						self.fast = True

					if self.direction != [-1, 0]:
						self.new_direction = [1, 0]
						self.move()

			elif event.type == pygame.KEYUP:
				if event.key in [119, 115, 97, 100, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
					self.fast = False

			elif event.type == pygame.MOUSEMOTION:
				self.menu_button.intersection(event.pos)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.menu_button.check_click(event.pos)

		# Псевдопоток логики
		if time.time() - self.timer > (0.1 if self.fast else 0.2):
			self.move()

		if self.updated:
			# Отрисовка поля
			self.game.screen.blit(self.game.files.images["game_field.png"], (0, 50))

			# Отрисовка змейки
			for elem, direction in zip(self.snake, self.snake_directions):
				if self.snake[0] != elem:
					self.game.screen.blit(pygame.transform.rotate(self.game.files.images["body.png"], self.angle_from_dir(direction)), (elem[0] * 25, elem[1] * 25 + 50))

				else:
					self.game.screen.blit(pygame.transform.rotate(self.game.files.images["head.png"], self.angle_from_dir(direction)), (elem[0] * 25, elem[1] * 25 + 50))

			# Отрисовка яблока
			self.game.screen.blit(self.game.files.images["apple.png"], (self.apple[0] * 25, self.apple[1] * 25 + 50))

			# Заливка топа
			pygame.draw.rect(self.game.screen, (130, 220, 150), (0, 0, 500, 50))

			# Кнопка "в меню"
			self.menu_button.draw(self.game.screen)
			
			# Отрисовка счёта
			self.game.screen.blit(self.score_text, self.score_text.get_rect())

			pygame.display.flip()
			self.updated = False
			# FIXME: Логика не может быть по времени меньше фпс, она на таймере а тут clock висит
		
		self.game.clock.tick(self.fps)
			