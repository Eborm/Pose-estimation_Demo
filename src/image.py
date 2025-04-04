import cv2
from vector2 import Vector2

class image():
	def __init__(self, image_path, pos, size):
		self.pos = pos
		self.size = size
		self.image = cv2.imread(image_path)
		if self.image is not None:
			self.image = cv2.resize(self.image, self.size.to_tuple())

	def draw(self, frame):
		if self.image is not None:
			frame[self.pos.y:self.pos.y + self.size.y, self.pos.x:self.pos.x + self.size.x] = self.image