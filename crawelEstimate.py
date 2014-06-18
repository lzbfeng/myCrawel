from TFDocument import *
from config import Config
def init():
	log = open('/home/hadoop/crawelData/xinli001/log.txt', 'r+')
	navis = {}
	docus = {}
	workers = {}
	Docus = []
	for line in log.readlines():
		contents = line.split('\t')
		if len(contents) == 4 and contents[2] == 'navigation:':
			worker = contents[1]
			navi = contents[3]
			if not workers.has_key(worker):
				workers[worker] = 1
			else:
				workers[worker] += 1
			if not navis.has_key(navi):
				navis[navi] = 1
			else:
				navis[navi] += 1
		if len(contents) == 6 and contents[2] == 'document:':
			worker = contents[1]
			docu = contents[3]
			docuFather = contents[4]
			if not workers.has_key(worker):
				workers[worker] = 1
			else:
				workers[worker] += 1

			docus[docu] = contents[4]
			Docus.append(Document(docu, contents[4], contents[5]))
			# print contents[5]


	return navis, docus, workers, Docus


def containStr(navis, key):
	contains = {}
	for navi in navis.items():
		if key in navi[0]:
			contains[navi[0]] = 1
	return contains

if __name__ == '__main__':
	navis, docus, workers, Docus = init()
	conf = Config()
	config = conf.getConfig()
	docusCtrl = DocusControl('/home/hadoop/crawelData/xinli001/data', Docus, config[0])
	docusCtrl.downloadDocus()
	# count = 0
	# if len(sys.argv) != 2:
	# 	print 'please input the key'
	# 	exit(1)
	# for contains in containStr(docus, sys.argv[1]):
	# 	count += 1
	# 	print count,
	# 	print contains
	# for worker in workers.items():
	# 	print worker
	fathers = {}
	contains = u'(news|cloud|mobile|sd|programmer)'
	notcontains = u'(http|csdn|\d+|net|html|www|rollingnews)'
	url = u'news'

	# for docu in docus.items():
	# 	# print docu
	# 	father = docu[1]
	# 	child = docu[0]
	# 	for j in [i.strip() for i in father.split('/')]:
	# 		for jj in [ii.strip() for ii in j.split('.')]:
	# 			url = jj
	# 			if re.match(notcontains, url) == None:
	# 				if not fathers.has_key(jj):
	# 					fathers[jj] = 1
	# 				else:
	# 					fathers[jj] += 1
	# for father in fathers.items():
	# 	print father
	# print len(docus)
	#
	# for docu in Docus:
	# 	print docu



