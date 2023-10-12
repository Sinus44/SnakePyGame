import pygame

class ImageButton:
	def __init__(self, x, y, image, oversize=1.2, use_center=True):
		self.x = x
		self.y = y
		self.image = image
		self.oversize = oversize
		self.use_center = use_center

		self.focused = False

		self.w = self.image.get_width()
		self.h = self.image.get_height()

		self.big_image = pygame.transform.scale(self.image, (self.w * self.oversize, self.h * self.oversize))

	def update(self):
		pygame.display.update(self.big_image.get_rect(centery=self.y, centerx=self.x))

	def draw(self, screen):
		if self.focused and self.oversize != 1:
			screen.blit(self.big_image, self.big_image.get_rect(center=(self.x, self.y)))
		else:
			screen.blit(self.image, self.image.get_rect(center=(self.x, self.y)))

	def intersection(self, pos):
		focused = self.x - self.w / 2 <= pos[0] <= self.x + self.w / 2 and self.y - self.h / 2 <= pos[1] <= self.y + self.h / 2
		
		if focused != self.focused:
			self.focused = focused
			if focused:
				self.on_focus()
			else:
				self.on_unfocus()
				
		return self.focused

	def check_click(self, pos):
		if self.on_click and self.intersection(pos):
			self.on_click()

	def on_click(self):
		...

	def on_focus(self):
		...

	def on_unfocus(self):
		...

class TextButton(ImageButton):
	def __init__(self, x, y, text, font, oversize=1.2, text_color=(255, 255, 255)):
		super().__init__(x, y, font.render(text or "BUTTON", True, text_color), oversize)
	
	


