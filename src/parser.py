from xml.sax import parse, SAXParseException, ContentHandler

class TagInfoHandler(ContentHandler):
	def __init__(self, tagName):
		ContentHandler.__init__(self)
		self.tagName = tagName
		self.isName = False
		self.content = []

	def getContent(self):
		return self.content

	def startElement(self, name, attributes):
		if name == self.tagName:
			self.isName = True

	def endElement(self, name):
		if name == self.tagName:
			self.isName = False

	def characters(self, content):
		content = content.strip()
		if content and self.isName:
			self.content.append(content)

