import os
from myUtils import *
from myFileOperation import *
from jobAndWorker import Job
from config import GLOBAL

class TaskTrace:
	def __init__(self, config, hashURLPath = 'hashurls.dat', jobQuenePath = 'jobquene.dat'):
		self.config = config
		self.websiteURL = config['startPageURL']
		if self.websiteURL == u'http://www.xinli001.com/':
			print self.websiteURL
		self.basepath = os.path.join(config['crawelBasePath'], config['name'])
		if not os.path.exists(self.basepath):
			os.mkdir(self.basepath)
		Log.setLogPath(os.path.join(self.basepath, 'log.txt'), os.path.join(self.basepath, 'errorlog.txt'))
		self.hashURLPath = os.path.join(self.basepath, hashURLPath)
		self.jobQuenePath = os.path.join(self.basepath, jobQuenePath)
		# urls we have getten
		self.hashURLs = {}
		self.loadhashURLs()
		# this is for the BFS method, this can provide restart function.
		self.jobQuene = []
		self.loadjobQuene()

	# judge whether the url has been visited
	def hasJob(self, job):
		return self.hashURLs.has_key(job.id)

	# log the url indecating we have get the url
	def logJob(self, job):
		Tools.mylock.acquire()
		if not self.hasJob(job):
			self.hashURLs[job.id] = None
		# save the visited urls
		if len(self.hashURLs) % 20 == 0:
			self.savehashURLs()
		Tools.mylock.release()

	def addJob(self, job):
		Tools.mylock.acquire()

		if not self.hasJob(job):
			# if job not in self.jobQuene:
			self.jobQuene.append(job)
			self.logJob(job)
			# save the remaining jobs
			if len(self.jobQuene) % 20 == 0:
				self.savejobQuene()

		Tools.mylock.release()

	def addJobs(self, jobList):
		for job in jobList:
			self.addJob(job)
		# for job in self.jobQuene:
		# 	print job.url
		# print self
	def assignOneJob(self, worker):
		Tools.mylock.acquire()
		if len(self.jobQuene) > 0:
			job = self.jobQuene.pop(0)
			worker.jobList.append(job)
			# print worker.name + ' get a job, url is: ' + job.url
			self.logJob(job)
		Tools.mylock.release()

	def assignJobs(self, countOfJobs, worker):
		if len(self.jobQuene) < countOfJobs:
			countOfJobs = len(self.jobQuene)
		for i in xrange(countOfJobs):
			self.assignOneJob(worker)


	def	savehashURLs(self):
		if self.hashURLPath:
			dumpObjToFile(self.hashURLs, self.hashURLPath)

	def loadhashURLs(self):
		path = self.hashURLPath
		if os.path.exists(path):
			self.hashURLs = loadObjFromFile(path)
		else:
			dumpObjToFile({}, self.hashURLPath)
			self.hashURLs = {}

	def savejobQuene(self):
		if self.jobQuenePath:
			dumpObjToFile(self.jobQuene, self.jobQuenePath)

	def loadjobQuene(self):
		path = self.jobQuenePath
		if os.path.exists(path):
			self.jobQuene = loadObjFromFile(path)
		else:
			job = Job([self.websiteURL, None, None])
			dumpObjToFile([job], self.jobQuenePath)
			self.jobQuene = [job]
			self.logJob(job)


	def countOfJobs(self):
		return len(self.jobQuene)

