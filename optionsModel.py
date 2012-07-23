class OptionsModel(object):
	def __init__(self):
		self.goesLeft = True
		self.launchOptions = True
		self.stopOnMouse = False
		self.syncTime = 3600
		self.speed = 50
		self.urls = []
	def getLeft(self):
		return self.goesLeft
	def getLaunch(self):
		return self.launchOptions
	def getStop(self):
		return self.stopOnMouse
	def getSync(self):
		return self.syncTime
	def getSpeed(self):
		return self.speed
	def getURLs(self):
		return self.urls
	def setLeft(self, val):
		self.goesLeft = val
	def setLaunch(self, val):
		self.launchOptions = val
	def setStop(self, val):
		self.stopOnMouse = val
	def setSync(self, val):
		self.syncTime = val
	def setSpeed(self, val):
		if val <= 100 and val >= 0:
			self.speed = val
		elif val < 0:
			self.speed = 0
		elif val > 100:
			self.speed = 100
