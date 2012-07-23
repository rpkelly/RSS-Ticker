import sys
import thread
import Tkinter as tk
import pygame as pg
import optionsModel
import optView
import tickerView

class Controller(object):
	def __init__(self):
		self.optModel = optionsModel.OptionsModel()
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
		file = open('options.xml', 'w')
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

if __name__ == "__main__":
	control = Controller()
