#! /usr/bin/python
#-*- coding: utf-8 -*-
import ConfigParser
import codecs
import re

class GLOBAL:
	websiteURL = 'http://www.csdn.net/'
	countOfGetURLs = 0
	exitList = []
	startTime = 0
	endTime = 0

class Config:

	def __init__(self, filePath = 'config.ini'):
		self.filePath = filePath
		self.config = []
		self.readConfig()

	def readConfig(self):
		config = {}
		for line in codecs.open(self.filePath, 'rb', 'utf').readlines():
			if re.match(u'\[.*\]', line.strip()):
				key = line.strip()[1:-1]
				config[key] = {}
		conf = ConfigParser.ConfigParser()
		conf.readfp(codecs.open(self.filePath, 'rb', 'utf'))
		for item in config.items():
			key = item[0]
			if key == u'basicConfig':
				item[1][u'crawelBasePath'] = conf.get(key, u'crawelBasePath')
				continue
			item[1][u'startPageURL'] = conf.get(key, u'startPageURL')
			item[1][u'document'] = conf.get(key, u'document')
			item[1][u'naviContains'] = conf.get(key, u'naviContains')
			item[1][u'naviNotContains'] = conf.get(key, u'naviNotContains')
			item[1][u'categories'] = conf.get(key, u'categories')
			item[1][u'countofThreads'] = int(conf.get(key, u'countofThreads'))
			item[1][u'timeout'] = int(conf.get(key, u'timeout'))
			item[1][u'starttimeout'] = int(conf.get(key, u'starttimeout'))
			item[1][u'endtimeout'] = int(conf.get(key, u'endtimeout'))
			item[1][u'name'] = key
			# print key
			# print conf.get(key, 'document')
			# print conf.get(key, 'naviContains')
			# print conf.get(key, 'naviNotContains')
		for item in config.items():
			if item[0] != u'basicConfig':
				item[1][u'crawelBasePath'] = config[u'basicConfig'][u'crawelBasePath']
				self.config.append(item[1])

	def getConfig(self):
		return self.config

if __name__ == '__main__':
	config = Config('config.ini')
	# print config.getConfig()
	for item in config.getConfig():
		print item