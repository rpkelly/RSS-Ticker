import sys
import pygame as pg
import controller

class TickerView(object):
	def __init__(self, controller):
		self.controller = controller
		self.screen = pg.display.set_mode((640,30))
		pg.display.set_caption("RSS Ticker")
		self.screen.fill((0,0,0))
		self.clock = pg.time.Clock()

		self.font = pg.font.Font(None, 25)

		self.text = self.font.render('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam condimentum blandit mi, pharetra ultricies ante gravida nec. Donec vehicula sodales eros, vitae scelerisque neque congue in. ', \
			True, (0,0,255), (0,0,0))
		self.text2 = self.text
		self.textRect = self.text.get_rect()
		self.textRect2 = self.text2.get_rect()

		self.textRect.x = self.screen.get_width()
		self.textRect.y = self.screen.get_height() -\
			self.textRect.height
		self.textRect2.x = self.screen.get_width() +\
			 self.textRect.width
		self.textRect2.y = self.screen.get_height() -\
			self.textRect2.height

		self.textRect.topleft = (self.textRect.x,\
			self.textRect.y)
		self.textRect2.topleft = (self.textRect2.x,\
			self.textRect2.y)

		self.speed =-1 * float(self.controller.optModel.getSpeed()) / 500.0

		self.curr_ticks = pg.time.get_ticks()
		self.screen.blit(self.text,self.textRect)
		self.screen.blit(self.text,self.textRect2)

	def notify(self, num):
		opts = self.controller.getCurrentOptions()
		if num:
			self.speed = float(opts["Speed"]) / 500.0
			if opts["Left"]:
				self.speed *= -1
			self.onMouse = opts["Stop"]

	def update(self):
		prev_ticks = self.curr_ticks
		self.curr_ticks = pg.time.get_ticks()
		ticks = self.curr_ticks - prev_ticks
		x = self.speed * ticks
		self.textRect.move_ip(x, 0)
		self.textRect2.move_ip(x, 0)
		if self.speed < 0:
			if (self.textRect.x + self.textRect.width) < 0:
				self.textRect.x = self.textRect2.x + self.textRect2.width
			if(self.textRect2.x + self.textRect2.width) < 0:
				self.textRect2.x = self.textRect.x + self.textRect.width
		else:
			if self.textRect.x > self.screen.get_width():
				self.textRect.x = -self.textRect.width + self.textRect2.x
			if self.textRect2.x > self.screen.get_width():
				self.textRect2.x = -self.textRect.width + self.textRect.x



	def runEventLoop(self):
		done = False
		while not done:
			self.clock.tick(40)
			for event in pg.event.get():
				if event.type == pg.QUIT: done = True
			self.screen.blit(self.text, self.textRect)
			self.screen.blit(self.text2, self.textRect2)
			self.update()
			pg.display.flip()
