import time
from threading import Timer
from jobAndWorker import Worker
from taskTrace import TaskTrace
from myUtils import *


class WorkerControl:

	def __init__(self, config, countOfWorkers = 100):
		self.config = config
		self.timeout = 20
		self.workerList = []
		for index in xrange(countOfWorkers):
			jobList = []
			worker = Worker('worker ' + str(index), self, config, jobList)
			print id(jobList)
			print 'I am ' + worker.name + ' and my joblist is: ' + str(id(worker.jobList))
			# print id(worker)
			self.workerList.append(worker)

		self.taskTrace = TaskTrace(config)
		print len(self.taskTrace.jobQuene)
		self.count = 0
		self.countOfWorkingWorkers = 0
		self.countOfJobsPerWorker = 1

	def addJob(self, job):
		self.taskTrace.addJob(job)
		# assign workers according to the workload
		# self.assignWorkers()

	def addJobs(self, jobList):
		self.taskTrace.addJobs(jobList)
		# assign workers according to the workload
		# self.assignWorkers()

	def assignWorkers(self):
		# Tools.mylock.acquire()
		countOfJobs = self.taskTrace.countOfJobs()

		if (self.countOfWorkingWorkers < len(self.workerList)) and (countOfJobs > len(self.workerList) * 5):
			self.awakeOtherWorkers()
		elif (self.countOfWorkingWorkers >= len(self.workerList)) and (countOfJobs < len(self.workerList) * 5):
			self.stopOtherWorkers()
		# Tools.mylock.release()
		# # start time
		# elif self.countOfWorkingWorkers == 0:
		# 	self.awakeOneWorker()


	def awakeOtherWorkers(self):
		# Tools.mylock.acquire()
		for index in xrange(len(self.workerList[1:])):
			workerindex = index + 1
			worker = self.workerList[workerindex]
			joblist = []
			newworker =	Worker(worker.name, self, self.config, joblist)
			self.workerList.remove(worker)
			self.workerList.insert(workerindex, newworker)
			Tools.mylock.acquire()
			self.countOfWorkingWorkers += 1
			Tools.mylock.release()
			newworker.setDaemon(True)
			newworker.start()
			print newworker.name + ' has been started'
		# for worker in self.workerList[1:]:
		# 	worker.setDaemon(True)
		# 	worker.start()
		# Tools.mylock.release()
		for worker in self.workerList[1:]:
			worker.join()

	def stopOtherWorkers(self):
		Tools.mylock.acquire()
		for worker in self.workerList[1:]:
			self.countOfWorkingWorkers -= 1
			worker.stop()
		Tools.mylock.release()

	def awakeOneWorker(self):
		first = self.workerList[0]
		if not first.isAlive():
			first.setDaemon(True)
			Tools.mylock.acquire()
			self.countOfWorkingWorkers = 1
			Tools.mylock.release()
			first.start()
			first.join()
			print 'awakeOneWorker'

	# child thread call this func to get some jobs
	def assignJobs(self, worker):
		countOfJobs = self.taskTrace.countOfJobs()
		if countOfJobs > 0:
			self.taskTrace.assignJobs(self.countOfJobsPerWorker, worker)
		else:
			print worker.name + ': There is not any jobs! I should sleep ' + str(self.config[u'endtimeout']) + ' seconds!!!'
			time.sleep(self.config[u'endtimeout'])
			if self.taskTrace.countOfJobs() <= 0:
				print worker.name + ': Really? I am off duty!!!'
				Tools.mylock.acquire()
				self.countOfWorkingWorkers -= 1
				Tools.mylock.release()
				worker.stop()
				worker.jobList.extend([])
			else:
				self.taskTrace.assignJobs(self.countOfJobsPerWorker, worker)

			# worker.stop()
			# self.countOfWorkingWorkers -= 1
		# self.assignWorkers()


	def startWork(self):
		# assign tasks according to the count of workers and count of jobs
		t = Timer(self.config[u'starttimeout'], self.awakeOtherWorkers)
		t.start()
		self.awakeOneWorker()
		# self.assignWorkers()



if __name__ == '__main__':
	t = time.time()
	# taskTrace = TaskTrace()
	workerControl = WorkerControl()
	workerControl.startWork()
	print 'time is: ' + str(time.time() - t)