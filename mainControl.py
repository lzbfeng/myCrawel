from multiprocessing import Process
from config import Config
from taskControl import WorkerControl

def func(websiteConfig):
	workerControl = WorkerControl(websiteConfig)
	workerControl.startWork()

if __name__ == '__main__':
	conf = Config('config.ini')
	config = conf.getConfig()
	processList = []
	for websiteConfig in config:
		print websiteConfig
		p = Process(target=func, args=(websiteConfig,))
		processList.append(p)
		p.start()

	for p in processList:
		p.join()