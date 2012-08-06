from xml.sax import parse, SAXParseException, ContentHandler

class TagInfoHandler(ContentHandler):
	def __init__(self):
		ContentHandler.__init__(self)
		self.isItem = False
		self.isTitle = False
		self.isLink = False
		self.tuples = []
		self.ndx = 0

	def getContent(self):
		return self.tuples

	def startElement(self, name, attributes):
		if name == "item":
			self.isItem = True
			self.tuples.append([None,None])
		elif name == "title" and self.isItem:
			self.isTitle = True
		elif name == "link" and self.isItem:
			self.isLink = True

	def endElement(self, name):
		if name == "item":
			self.isItem = False
			self.ndx += 1
		elif name == "title":
			self.isTitle = False
		elif name == "link":
			self.isLink = False

	def characters(self, content):
		content = content.strip()
		if content and self.isItem and self.isTitle:
			self.tuples[self.ndx][0] = content
		elif content and self.isItem and self.isLink:
			self.tuples[self.ndx][1] = content

