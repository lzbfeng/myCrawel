import os
import re
from myUtils import Log, Tools
from TFThread import TFThread
from myUrllib import *
from myFileOperation import *

class Document:

	def __init__(self, url, fatherurl, name):
		self.url = url
		self.fatherURL = fatherurl
		self.name = Tools.replaceSpecialCharacters(name.strip())
		self.basepath = None
		self.path = None

	def setPath(self, basepath):
		self.path = os.path.join(basepath, self.name.decode('utf-8') + u'.html')
		# Log.printAndLog(self.path + '\n' + self.url + '\n')
		# print self.path
		# print self.url
	def __str__(self):
		return "%s\t%s\t%s"%(self.url, self.fatherURL, self.name)

class DocusControl:

	def __init__(self, basePath, docus, config):
		Log.setLogPath(os.path.join(basePath, 'downloadlog.txt'), os.path.join(basePath, 'downloaderrorlog.txt'))
		self.basePath = basePath
		if not os.path.exists(basePath):
			os.mkdir(basePath)
		self.docus = docus
		self.config = config
		self.generateDirs()
		self.workers = []
		self.countofDownloaded = 0
		self.downloadedDocus= {}
		self.downloadedDocusPath = os.path.join(self.basePath, 'downloadedDocus.dat')
		self.countofThreads = config[u'countofThreads']
		self.timeout = config[u'timeout']
		self.loadDownloadedDocus()

	def categoryFilter(self):
		contains = u'(news|cloud|mobile|sd|programmer)'
		notcontains = u'(http|csdn|\d+|net|html|www|rollingnews)'
		return contains, notcontains

	def loadDownloadedDocus(self):
		if not os.path.exists(self.downloadedDocusPath):
			dumpObjToFile({}, self.downloadedDocusPath)
			self.downloadedDocus = {}
		else:
			self.downloadedDocus = loadObjFromFile(self.downloadedDocusPath)
		self.countofDownloaded = len(self.downloadedDocus)

	def saveDownloadedDocus(self):
		Tools.mylock.acquire()
		dumpObjToFile(self.downloadedDocus, self.downloadedDocusPath)
		Tools.mylock.release()

	def parseCategories(self):
		return [i.strip() for i in self.config[u'categories'].split(u'\t')]

	def generateDirs(self):
		contains, notcontains = self.categoryFilter()

		paths = {}
		for docu in self.docus:
			fatherurl = docu.fatherURL
			filters = self.parseCategories()
			for filter in filters:
				myItems = re.findall(filter, fatherurl, re.S)
				if len(myItems) == 0:
					continue
				path = myItems[0]
				if path == u'info':
					print fatherurl
				if not paths.has_key(path):
					paths[path] = 1
				else:
					paths[path] += 1

				docu.setPath(os.path.join(self.basePath, path))
				break
		docus = []
		for docu in self.docus:
			if docu.path != None:
				docus.append(docu)
		self.docus = docus
		for path in paths.items():
			print path
			path = os.path.join(self.basePath, path[0])
			if not os.path.exists(path):
				os.mkdir(path)

	def download(self, start, end, threadName = ''):
		downloadList = self.docus[start:end]
		for docu in downloadList:
			if self.downloadedDocus.has_key(Tools.getMD5(docu.url)):
				continue
			self.downloadedDocus[Tools.getMD5(docu.url)] = None
			try:
				req = getResponse(docu.url)
				response = urllib2.urlopen(req, timeout=self.timeout)
				self.saveDocu(response.read(), docu.path)
				Tools.mylock.acquire()
				self.countofDownloaded += 1
				if self.countofDownloaded % 30 == 0:
					self.saveDownloadedDocus()
				Tools.mylock.release()
				msg = str(self.countofDownloaded) + '\t' + threadName + '\t' + docu.url + '\t' + docu.name + '\n'
				Log.printAndLog(msg)

			except Exception, e:
				msg = threadName + ':\t' + 'there is an error occur when use the function: DocusControl.download and it is: ' + str(e)
				msg += '\nthe url is: ' + docu.url + '\t' + docu.name + '\n'
				Log.printAndLog(msg, True)

	def saveDocu(self, obj, path):
		Tools.mylock.acquire()
		saveFile = open(path, 'w+')
		saveFile.write(obj)
		saveFile.close()
		Tools.mylock.release()

	def downloadDocus(self):
		countOfDocus = len(self.docus)
		countOfThreads = self.countofThreads
		perThread = countOfDocus / (countOfThreads - 1)
		yu = countOfDocus % countOfThreads
		for index in xrange(countOfThreads):
			start = index * perThread
			if index != countOfThreads - 1:
				end = (index + 1)* perThread
			else:
				end = countOfDocus
			worker1 = TFThread(str(index) + ' worker', self.download, start, end)
			worker1.setDaemon(True)
			worker1.start()
			self.workers.append(worker1)

		for worker in self.workers:
			worker.join()
	def getDocus(self):
		return self.docus




