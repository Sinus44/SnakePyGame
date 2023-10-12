import pygame
import os

class Files:
	def __init__(self, images_path="images", sounds_path="sounds", fonts_path="fonts", assets_path="../assets"):
		self.images_path = images_path + ("/" if images_path[-1] != "/" and images_path else "")
		self.sounds_path = sounds_path + ("/" if images_path[-1] != "/" and sounds_path else "")
		self.fonts_path = fonts_path + ("/" if images_path[-1] != "/" and fonts_path else "")
		self.assets_path = assets_path + ("/" if assets_path[-1] != "/" and assets_path else "")

		self.images = {}
		self.fonts = {}
		self.sounds = {}

	def load_images(self):
		self.images = {}

		for image in os.listdir(self.assets_path + self.images_path):
			try:
				self.images[image] = pygame.image.load(self.assets_path + self.images_path + image)

			except:
				print(f"Warn: File {self.assets_path + self.images_path + image} loading error")
				continue

	def load_fonts(self, size=36):
		self.fonts = {}
		pygame.font.init()

		for font in os.listdir(self.assets_path + self.fonts_path):
			self.fonts[font] = pygame.font.Font(self.assets_path + self.fonts_path + font, size)

	def load_sounds(self):
		self.sounds = {}
		pygame.mixer.init()

		for sound in os.listdir(self.assets_path + self.sounds_path):
			dot = sound.index(".")
			file_name = sound[:dot]
			
			if file_name == "music":
				pygame.mixer.music.load(self.assets_path + self.sounds_path + sound)
			else:
				self.sounds[sound] = pygame.mixer.Sound(self.assets_path + self.sounds_path + sound)



