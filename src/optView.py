import controller
import Tkinter as tk

class OptView(object):
	def __init__(self, controller):
#		print "Opt init"
		self.controller = controller
		self.controller.optView = self
		root = tk.Tk()
		self.inVar = tk.StringVar()
		self.refVar = tk.IntVar()
		self.launchVar = tk.IntVar()
		self.slideVar = tk.IntVar()
		self.stopVar = tk.IntVar()
		self.leftVar = tk.IntVar()
		self.size = tk.IntVar()
		self.x = tk.IntVar()
		self.y = tk.IntVar()

		self.refVar.set(self.controller.optModel.getSync())
		self.launchVar.set(self.controller.optModel.getLaunch())
		self.slideVar.set(self.controller.optModel.getSpeed())
		self.size.set(self.controller.optModel.getSize())
		self.stopVar.set(self.controller.optModel.getStop())
		self.leftVar.set(self.controller.optModel.getLeft())
		self.x.set(self.controller.optModel.getLoc()[0])
		self.y.set(self.controller.optModel.getLoc()[1])

		row0 = tk.Frame(root)
		row1 = tk.Frame(root)
		row2 = tk.Frame(root)
		listRow = tk.Frame(root)
		row3 = tk.Frame(root)
		row4 = tk.Frame(root)
		row5 = tk.Frame(root)
		row6 = tk.Frame(root)
		row7 = tk.Frame(root)
		row8 = tk.Frame(root)


		label = tk.Label(row0,  \
			text = "RSS Ticker Options", \
			font = ("serif", 16))
		label.pack(side = tk.TOP)

		self.box = tk.Checkbutton(row1, \
			text = "Launch Options On Start", \
			variable = self.launchVar)
		self.box.pack(side = tk.TOP)

		label = tk.Label(row2, \
			text = "Input URL:")
		self.feedEntry = tk.Entry(row2, \
			 textvariable = self.inVar)
		label.pack(side = tk.LEFT)
		self.feedEntry.pack(side = tk.LEFT)
		self.feedEntry.bind("<Return>", lambda event:controller.appendURL())

		label = tk.Label(listRow, \
			text = "Feeds:")
		label.pack(side = tk.LEFT)
		self.listbox = tk.Listbox(listRow)
		self.listbox.pack(side = tk.LEFT)
		for url in self.controller.optModel.getURLs():
			self.listbox.insert(tk.END, url)
		button = tk.Button(listRow, text="Remove Feed", command=self.delete)
		button.pack(side = tk.LEFT)
		self.listbox.bind("<Delete>", lambda event:self.delete())

		label = tk.Label(row3, \
			text = "Ticker Speed:")
		self.slider = tk.Scale(row3, \
			from_ = 0, to = 100, \
			variable = self.slideVar, \
			orient = tk.HORIZONTAL)
		label.pack(side = tk.LEFT)
		self.slider.pack(side = tk.LEFT)


		self.stopBox = tk.Checkbutton(row4, \
			text = "Stop Ticker on Mouse Over", \
			variable = self.stopVar)
		self.stopBox.pack(side = tk.TOP)

		label = tk.Label(row5, \
			text = "Refresh Feed Items")
		self.refEntry = tk.Entry(row5, \
			textvariable = self.refVar)
		label.pack(side = tk.LEFT)
		self.refEntry.pack(side = tk.LEFT)
		label = tk.Label(row5, text = "sec")
		label.pack(side = tk.RIGHT)

		label = tk.Label(row6, \
			text = "Direction:")
		label.pack(side = tk.LEFT)
		radio1 = tk.Radiobutton(row6, \
			text = "RtL", variable = self.leftVar, \
			value = 1)
		radio2 = tk.Radiobutton(row6, \
			text = "LtR", variable = self.leftVar, \
			value = 0)
		radio1.pack(side = tk.LEFT)
		radio2.pack(side = tk.LEFT)

		label = tk.Label(row7, \
			text = "Ticker Size:")
		self.slider2 = tk.Scale(row7, \
			from_ = 0, to = 100, \
			variable = self.size, \
			orient = tk.HORIZONTAL)
		print self.controller.optModel.getSize()
		label.pack(side = tk.LEFT)
		self.slider2.pack(side = tk.LEFT)

		label = tk.Label(row8, \
			text = "X Y Location")
		entry = tk.Entry(row8, \
			textvariable = self.x)
		label.pack(side = tk.LEFT)
		entry.pack(side = tk.LEFT)
		entry = tk.Entry(row8, \
			textvariable = self.y)
		entry.pack(side = tk.LEFT)

		row0.pack(side = tk.TOP)
		row1.pack(side = tk.TOP)
		row2.pack(side = tk.TOP)
		listRow.pack(side = tk.TOP)
		row3.pack(side = tk.TOP)
		row4.pack(side = tk.TOP)
		row5.pack(side = tk.TOP)
		row6.pack(side = tk.TOP)
		row7.pack(side = tk.TOP)
		row8.pack(side = tk.TOP)

		button = tk.Button(root, text="Save/Apply")
		button.configure(command = self.controller.save)
		button.pack(side = tk.LEFT)
		button = tk.Button(root, text = "Quit")
		button.configure(command = lambda: self.quit(root))
		button.pack(side = tk.LEFT)
		button = tk.Button(root, text = "Close All")
		button.configure(command = lambda: self.exit())
		button.pack(side = tk.LEFT)

		root.protocol("WM_DELETE_WINDOW", lambda: self.quit(root))
		tk.mainloop()

	def delete(self):
		self.listbox.delete(tk.ANCHOR)
		del self.controller.optModel.getURLs()[:]
		ndx = 0
		while ndx < self.listbox.size():
			self.controller.optModel.getURLs().append(self.listbox.get(ndx))
			ndx += 1
		self.controller.save()

	def quit(self, root):
		self.controller.viewExists = False
		root.destroy()

	def exit(self):
		self.controller.tickerView.done = True

	def getX(self):
		return self.x.get()

	def getY(self):
		return self.y.get()

	def getSize(self):
		return self.size.get()

	def getLeft(self):
		return self.leftVar.get()

	def getLaunch(self):
		return self.launchVar.get()

	def getStop(self):
		return self.stopVar.get()

	def getSync(self):
		return self.refVar.get()

	def getSpeed(self):
		return self.slideVar.get()

	def getURL(self):
		return self.inVar.get()

if __name__ == "__main__":
	View = OptView()
	tk.mainloop()		
