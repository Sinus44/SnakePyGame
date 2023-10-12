import pygame

class Inputbox:
	def __init__(self, x, y, w, h, font, text="", max_length=20):
		self.x = x 
		self.y = y
		self.w = w
		self.h = h
		self.font = font
		self.text = text
		self.selected = False
		self.rendered = None
		self.max_length = max_length
		self.cursor_counter = 0
		self.cursor_enable = False 

		self.regenerate_text()

	def _on_select_(self):
		self.on_select()
		self.cursor_counter = -1
		self.cursor_enable = False		

	def _on_unselect_(self):
		self.on_unselect()
		self.cursor_counter = 0
		self.cursor_enable = False
		self.regenerate_text()

	def on_select(self):
		...

	def on_unselect(self):
		...

	def intersection(self, pos):
		selected = self.x <= pos[0] <= self.x + self.w and self.y - self.h <= pos[1] <= self.y + self.h

		if selected != self.selected:
			if selected:
				self._on_select_()

			else:
				self._on_unselect_()
				
		self.selected = selected
		return self.selected

	def regenerate_text(self, is_cursor=False):
		self.rendered = self.font.render(self.text + ("I" if self.cursor_enable and self.selected else ""), True, (255, 255, 255))

	def input(self, symbol, is_delete=False):
		if not self.selected: return

		if is_delete:
			self.text = self.text[:-1]
			self.regenerate_text()
		else:
			if len(self.text) < self.max_length:
				self.text += symbol
				self.regenerate_text()

	def draw(self, screen):
		self.cursor_counter += 1
		self.cursor_counter = self.cursor_counter % 20

		if self.selected and self.cursor_counter == 0:
			self.cursor_enable = not self.cursor_enable
			self.regenerate_text()

		pygame.draw.rect(screen, (150, 200, 200), (self.x, self.y, self.w, self.h))
		screen.blit(self.rendered, self.rendered.get_rect(left=self.x, top=self.y))


