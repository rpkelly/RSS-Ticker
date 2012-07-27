import sys
import webbrowser
import pygame as pg
import controller
import os
import Tkinter as tk

class TickerView(object):
	def __init__(self, controller):
# To be used for phase IV
#		r = tk.Tk()
#		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0,r.winfo_screenheight()-30)
		self.controller = controller
		self.screen = pg.display.set_mode((640,30))#, pg.NOFRAME) #For phase IV
		pg.display.set_caption("RSS Ticker")
		self.screen.fill((0,0,0))
		self.clock = pg.time.Clock()

		self.font = pg.font.Font(None, 25)
		ndx = 0;
		self.rects = []
		self.text = []
		for title in self.controller.rssModel.getTitles():
			if ndx == 0:
				self.makeRect(0)
				self.screen.blit(self.text[0], self.rects[0])
			else:
				self.makeRect(ndx, self.rects[ndx-1])
				self.screen.blit(self.text[ndx], self.rects[ndx])
			ndx += 1

		self.speed =-1 * float(self.controller.optModel.getSpeed()) / 500.0

		self.curr_ticks = pg.time.get_ticks()

	def makeRect(self, ndx, prevRect=pg.Rect(0,0,0,0)):
		t = self.font.render(self.controller.rssModel.getTitles()[ndx], True, (0,0,255), (0,0,0))
		self.text.append(t)
		rect = t.get_rect()
		if prevRect.x != 0:
			rect.x = prevRect.x + (prevRect.width + 30)
		else:
			rect.x = self.screen.get_width()
		rect.y = self.screen.get_height() - rect.height
		rect.topleft = (rect.x, rect.y)
		self.rects.append(rect)



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
		for rect in self.rects:
			rect.move_ip(x, 0)
		ndx = 0
		if self.speed < 0:
			for rect in self.rects:
				if (rect.x + rect.width) < 0:
					rect.x = self.rects[ndx-1].x + (self.rects[ndx-1].width + 30)
					rect.topleft = (rect.x, rect.y)
				ndx += 1
		else:
			for rect in self.rects:
				if rect.x > self.screen.get_width():
					rect.x = -self.rects[ndx].width + (self.rects[ndx-1].x - 30 )
				ndx += 1

	def runEventLoop(self):
		done = False
		isPaused = False
		while not done:
			self.clock.tick(40)
			speed = self.controller.optModel.getSpeed()
			for event in pg.event.get():
				if event.type == pg.QUIT: done = True
				if event.type == pg.MOUSEMOTION:
					if self.controller.optModel.getStop():
						if event.pos[1] > 5 and event.pos[1] < 25:
							isPaused = True
							if isPaused:
								self.clock.tick(40)
							while isPaused:
								self.controller.optModel.setSpeed(0)
								for event in pg.event.get():
									if event.type == pg.MOUSEMOTION:
										if event.pos[1] < 5 or event.pos[1] > 25:
											self.controller.optModel.setSpeed(speed)
											isPaused = False
				if event.type == pg.MOUSEBUTTONDOWN:
					ndx = 0
					for rect in self.rects:
						if rect.collidepoint(event.pos):
							webbrowser.open(self.controller.rssModel.getLinks()[ndx], 2)
						ndx += 1
			ndx = 0
			for rect in self.rects:
				if rect.x < self.screen.get_width() and (rect.x + rect.width) > 0:
					self.screen.blit(self.text[ndx], rect)
				ndx+=1
			self.update()
			pg.display.flip()

