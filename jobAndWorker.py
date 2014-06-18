# -* - coding: UTF-8 -* -
import threading
from threading import Timer
from myUtils import *
from pager import *
from config import GLOBAL

class Job:
	def __init__(self, taskURL, otherInfo = None):
		self.url = taskURL[0]
		self.furl = taskURL[1]
		self.title = taskURL[2]
		self.id = Tools.getMD5(self.url)
		self.otherInfo = otherInfo


class Worker(threading.Thread):
	def __init__(self, name, workerCtrl, config, jobList = []):
		threading.Thread.__init__(self)
		self.name = name
		self.jobList = jobList
		self.workerCtrl = workerCtrl
		self.state = 0
		self.config = config
	# def killself(self):
	# 	exit(1)

	def callJob(self, timeout = 5):
		# t = Timer(timeout, self.killself)
		# t.start()
		self.workerCtrl.assignJobs(self)
		# t.cancel()

	def addToJobQuene(self, urls):
		jobList = []
		for url in urls:
			jobList.append(Job(url))
		self.workerCtrl.addJobs(jobList)

	def work(self):

		# if there is not any job, call job from workerControl
		url = ''
		try:
			print self.name + ' call a job from boss...'
			self.callJob()
			if len(self.jobList) != 0:
				print self.name + ' get a job!'
			for job in self.jobList:
				url = job.url
				if url == u'http://www.xinli001.com/daka/780/study/':
					print 'aaaaaaaa'
				pager = generateOnePager(job.url, self.config)

				Tools.mylock.acquire()
				GLOBAL.countOfGetURLs += 1
				Tools.mylock.release()
				print GLOBAL.countOfGetURLs
				if pager.isDocument():
					Log.printAndLog(str(GLOBAL.countOfGetURLs) + '\t' + self.name + '\tdocument:\t' + url +\
									'\t' + job.furl + '\t' + job.title + '\n')
				elif pager.isNavigation():
					Log.printAndLog(str(GLOBAL.countOfGetURLs) + '\t' + self.name + '\tnavigation:\t' + url + '\n')
					urls = pager.getPageURLs()

					self.addToJobQuene(urls)
				msg = 'count of jobs: ' + str(self.workerCtrl.taskTrace.countOfJobs()) + '\n'
				msg += 'count of working workers: ' + str(self.workerCtrl.countOfWorkingWorkers)
				# Log.printAndLog(msg)
				print msg
		except Exception, e:
			Log.printAndLog('there is a error occured: ' + str(e) + '. The url is:\t' + url + '\n', True)

		for job in self.jobList:
			self.jobList.remove(job)

	def run(self):
		self.state = 1
		while(self.state == 1):
			self.work()

	def stop(self):
		if self.isAlive():
			self.state = 0

