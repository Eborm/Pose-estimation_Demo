import cv2
import time

class Button:
	def __init__(self, text, text_color, x, y, width, height, color, hover_color, action=None):
		self.text =text
		self.text_color = text_color
		self.x, self.y = x, y
		self.width, self.height = width, height
		self.color, self.standard_color,self.hover_color = color, color, hover_color
		self.action=action
		
		self.cooldown_lenght = 2
		self.cooldown_enabled = False
		self.cooldown_start_time = None

		self.hover_cooldown_lenght = 3
		self.hover_enabled = False
		self.hover_start_time = None

		self.not_hovering = 3
		self.not_hovering_start_time = None

		b_stand, g_stand, r_stand = self.color
		b_targ, g_targ, r_targ = self.hover_color
		self.b_inc = (b_targ - b_stand) / self.hover_cooldown_lenght if (b_targ - b_stand) != 0 else 0
		self.g_inc = (g_targ - g_stand) / self.hover_cooldown_lenght if (g_targ - g_stand) != 0 else 0
		self.r_inc = (r_targ - r_stand) / self.hover_cooldown_lenght if (r_targ - r_stand) != 0 else 0

	def draw(self, frame):
		cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), self.color, -1)
		cv2.putText(frame, self.text, (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.text_color, 2)

	def hover_time_handler(self):
		if self.hover_start_time == None:
			self.hover_start_time = time.time()
			self.not_hovering_start_time = None
		elif time.time() - self.hover_start_time > self.hover_cooldown_lenght:
			self.hover_enabled = True
			self.hover_start_time = None

	def not_hovering_handler(self):
		if self.not_hovering_start_time == None:
			self.not_hovering_start_time = time.time()
		elif time.time() - self.not_hovering_start_time > self.not_hovering:
			self.not_hovering_start_time = None
			self.hover_start_time = None
			self.hover_enabled = False
			self.color = self.standard_color

	def button_cooldown_handler(self):
		self.cooldown_start_time = time.time()
		self.cooldown_enabled = True
		self.hover_enabled = False
		self.color = self.standard_color
		self.action()

	def animate_color(self):
		if self.hover_start_time != None:
			elapsed_time = time.time() - self.hover_start_time
			if elapsed_time == 0:
				pass
			else:
				new_b = max(0, min(255, int(self.standard_color[0] + self.b_inc * elapsed_time)))
				new_g = max(0, min(255, int(self.standard_color[1] + self.g_inc * elapsed_time)))
				new_r = max(0, min(255, int(self.standard_color[2] + self.r_inc * elapsed_time)))
				self.color = (new_b, new_g, new_r)

	def button_handler(self, hand_results, h, w):
		if self.cooldown_enabled:
			if time.time() - self.cooldown_start_time > self.cooldown_lenght:
				self.cooldown_enabled = False
		elif hand_results.multi_hand_landmarks and self.action != None:
			for hand_landmarks in hand_results.multi_hand_landmarks:
				for lm in hand_landmarks.landmark:
					cx, cy = int(lm.x * w), int(lm.y * h)
					if self.x < cx < (self.x + self.width) and self.y < cy < (self.y + self.height):
						if self.hover_enabled:
							self.button_cooldown_handler()
						elif not self.hover_enabled:
							self.animate_color()
							self.hover_time_handler()
					else:
						self.not_hovering_handler()