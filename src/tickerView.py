import sys
import webbrowser
import pygame as pg
import controller
import os
import Tkinter as tk

class TickerView(object):
	def __init__(self, controller):
#		r = tk.Tk()
		self.controller = controller
		self.screensize = pg.display.Info().current_h
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (self.controller.optModel.getLoc())
		self.screen = pg.display.set_mode(((self.screensize * self.controller.optModel.getSize())/100, 30), pg.NOFRAME)
		pg.display.set_caption("RSS Ticker")
		self.screen.fill((0,0,0))
		self.clock = pg.time.Clock()

		self.font = pg.font.Font(None, 25)
		self.rects = []
		self.text = []

		self.makeLinks()
		self.speed =-1 * float(self.controller.optModel.getSpeed()) / 500.0

		self.curr_ticks = pg.time.get_ticks()

	def makeLinks(self):
		del self.rects[:]
		del self.text[:]
		ndx = 0;
		for title in self.controller.rssModel.getTuples():
			if ndx == 0:
				self.makeRect(0)
				self.screen.blit(self.text[0], self.rects[0])
			else:
				self.makeRect(ndx, self.rects[ndx-1])
				self.screen.blit(self.text[ndx], self.rects[ndx])
			ndx += 1

	def makeRect(self, ndx, prevRect=pg.Rect(0,0,0,0)):
		t = self.font.render(self.controller.rssModel.getTuples()[ndx][0], True, (8,232,222), (0,0,0))
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
		if num == 1:
			self.speed = float(opts["Speed"]) / 500.0
			if opts["Left"]:
				self.speed *= -1
			self.onMouse = opts["Stop"]
		elif num == 2:
			self.makeLinks()

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

	def openLinks(self, pos):
		ndx = 0
		for rect in self.rects:
			if rect.collidepoint(pos):
				webbrowser.open(str(self.controller.rssModel.getTuples()[ndx][1]), 0)
				del self.rects[ndx]
				del self.controller.rssModel.getTuples()[ndx]
				del self.text[ndx]
			ndx += 1

	def runEventLoop(self):
		self.done = False
		isPaused = False
		while not self.done:
			self.clock.tick(40)
			speed = self.controller.optModel.getSpeed()
			for event in pg.event.get():
				if event.type == pg.QUIT: self.done = True
				elif event.type == pg.MOUSEMOTION:
					if self.controller.optModel.getStop():
						if event.pos[1] > 5 and event.pos[1] < 25 and event.pos[0] > 5 and event.pos[0] < 635:
							isPaused = True
						else:
							isPaused = False
				if event.type == pg.MOUSEBUTTONDOWN:
						if event.button == 1:
							self.openLinks(event.pos)
						else:
							print "Detect Right"
							if not self.controller.viewExists:
								print "Should Open"
								self.controller.createOpt()
			ndx = 0
			self.screen.fill((0,0,0))
			for rect in self.rects:
				if rect.x < self.screen.get_width() and (rect.x + rect.width) > 0:
					self.screen.blit(self.text[ndx], rect)
				ndx+=1
			if not isPaused:
				self.update()
			pg.display.flip()

