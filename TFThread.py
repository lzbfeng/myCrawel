import threading
from threading import Timer

class TFThread(threading.Thread):
	def __init__(self, name, func, start, end):
		threading.Thread.__init__(self)
		self.name = name
		self.startPoint = start
		self.endPoint = end
		self.func = func

	def run(self):
		self.func(self.startPoint, self.endPoint, self.name)

