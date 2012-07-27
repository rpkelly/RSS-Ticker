import sys
import os
import urllib2
import thread
import time
import Tkinter as tk
import pygame as pg
import parser
import optionsModel
import rssModel
import optView
import tickerView
from xml.sax import parse, SAXParseException, ContentHandler

class Controller(object):
	def __init__(self):
		self.optModel = optionsModel.OptionsModel()
		self.readOptions()
		self.rssModel = rssModel.RSSModel()
		self.downloadRSS()
		try:
			thread.start_new_thread(self.readThread,())
		except:
			print "Unable to read RSS links"
		self.optView = optView.OptView(self)
		try:
			thread.start_new_thread(self.startPG,())
		except:
			print "Unable to start ticker"
		tk.mainloop()	

	def startPG(self):
		pg.init()
		self.tickerView = tickerView.TickerView(self)
		self.tickerView.notify(1)
		self.tickerView.runEventLoop()

	def setNewOptions(self):
		self.optModel.setLeft(self.optView.getLeft())
		self.optModel.setLaunch(self.optView.getLaunch())
		self.optModel.setStop(self.optView.getStop())
		self.optModel.setSync(self.optView.getSync())
		self.optModel.setSpeed(self.optView.getSpeed())
		self.tickerView.notify(1)

	def getCurrentOptions(self):
		options = {}
		options["Left"] = self.optModel.getLeft()
		options["Launch"] = self.optModel.getLaunch()
		options["Stop"] = self.optModel.getStop()
		options["Sync"] = self.optModel.getSync()
		options["Speed"] = self.optModel.getSpeed()
		options["URL"] = self.optModel.getURLs()
		return options

	def appendURL(self):
		self.optModel.getURLs().append( \
			self.optView.getURL())
		self.optView.feedEntry.delete(0,tk.END)

	def save(self):
		file = open('./data/options.xml', 'w')
		print >> file, '<options>'
		self.setNewOptions()
		opts = self.getCurrentOptions()
		for key in opts:
			if key != "URL":
				print >> file, '	<' + str(key) + '>' + \
					str(opts[key]) + '</' + str(key) + '>'
			else:
				print >> file, '	<urls>'
				for entry in opts[key]:
					print >> file, '		<url>' + \
						entry + '</url>'
				print >> file, '	</urls>'
		print >> file, '</options>'
		file.close()

	def quit(self):
		sys.exit()

	def readOptions(self):
		file = open('./data/options.xml', 'r')
		element = parser.TagInfoHandler('Left')
		try:
			parse(file, element)
		except:
			print "Parse failure"
		if element.getContent():
			self.optModel.setLeft(int(float(element.getContent()[0])))
		element = parser.TagInfoHandler('Launch')
		file = open('./data/options.xml', 'r')
		try:
			parse(file, element)
		except:
			print "Parse failure"
		if element.getContent():
			self.optModel.setLaunch(int(float(element.getContent()[0])))
		element = parser.TagInfoHandler('Stop')
		file = open('./data/options.xml', 'r')
		try:
			parse(file, element)
		except:
			print "Parse failure"
		if element.getContent():
			self.optModel.setStop(int(float(element.getContent()[0])))
		element = parser.TagInfoHandler('Sync')
		file = open('./data/options.xml', 'r')
		try:
			parse(file, element)
		except:
			print "Parse failure"
		if element.getContent():
			self.optModel.setSync(float(element.getContent()[0]))
		element = parser.TagInfoHandler('Speed')
		file = open('./data/options.xml', 'r')
		try:
			parse(file, element)
		except:
			print "Parse failure"
		if element.getContent():
			self.optModel.setSpeed(float(element.getContent()[0]))
		element = parser.TagInfoHandler('url')
		file = open('./data/options.xml', 'r')
		try:
			parse(file, element)
		except:
			print "Parse failure"
		urls = element.getContent()
		for url in urls:
			self.optModel.getURLs().append(url)
		file.close()

	def readRSS(self):
		file = open('./data/feeds.rss', 'r')
		titles = self.rssModel.getTitles()
		links = self.rssModel.getLinks()
		del titles[:]
		del links[:]
		element = parser.TagInfoHandler('title')
		try:
			parse(file, element)
			print "Parsed titles"
		except SAXParseException, message:
			print "Parse failure", message
		titles.extend(element.getContent())
		element = parser.TagInfoHandler('link')
		file = open('./data/feeds.rss', 'r')
		try:
			parse(file, element)
			print "Parsed links"
		except:
			print "Parse failure"
		links.extend(element.getContent())

	def readThread(self):
		while True:
			self.downloadRSS()
			time.sleep(self.optModel.getSync())

	def downloadRSS(self):
		urls = self.optModel.getURLs()
		file = open('./data/feeds.rss', 'w')
		print >> file, "<feeds>"
		for url in urls:
			page = urllib2.urlopen(url)
			line = page.readline()
			line = page.readline()
			while line:
				line.rstrip()
				print >> file, line
				line = page.readline()
			page.close()
		print >> file, "</feeds>"
		file.close()
		self.readRSS()



if __name__ == "__main__":
	control = Controller()

