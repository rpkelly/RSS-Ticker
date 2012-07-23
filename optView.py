import controller
import Tkinter as tk

class OptView(object):
	def __init__(self, controller):
		self.controller = controller
		root = tk.Tk()
		self.inVar = tk.StringVar()
		self.refVar = tk.IntVar()
		self.launchVar = tk.IntVar()
		self.slideVar = tk.DoubleVar()
		self.stopVar = tk.IntVar()
		self.leftVar = tk.IntVar()

		row0 = tk.Frame(root)
		row1 = tk.Frame(root)
		row2 = tk.Frame(root)
		row3 = tk.Frame(root)
		row4 = tk.Frame(root)
		row5 = tk.Frame(root)
		row6 = tk.Frame(root)


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

		label = tk.Label(row3, \
			text = "Ticker Speed:")
		self.slider = tk.Scale(row3, \
			from_ = 0, to = 100, \
			variable = self.slideVar, \
			orient = tk.HORIZONTAL)
		label.pack(side = tk.LEFT)
		self.slider.pack(side = tk.LEFT)

		self.stopBox = tk.Checkbutton(row4, \
			text = "Stop Ticker on Mouse Over (Not Implemented)", \
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

		row0.pack(side = tk.TOP)
		row1.pack(side = tk.TOP)
		row2.pack(side = tk.TOP)
		row3.pack(side = tk.TOP)
		row4.pack(side = tk.TOP)
		row5.pack(side = tk.TOP)
		row6.pack(side = tk.TOP)

		button = tk.Button(root, text="Save/Apply")
		button.configure(command = self.controller.save)
		button.pack(side = tk.LEFT)
		button = tk.Button(root, text = "Quit")
		button.configure(command = self.controller.quit)
		button.pack(side = tk.LEFT)

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
