# -*- coding: utf-8 -*-
#===============================================================================
# 目的：为其他的模块提供一些通用的工具
# 作者：terry_feng
# 时间：2014.4.23-8.28
#===============================================================================
import threading
import codecs
import md5


class Tools():
	#线程锁
	mylock = threading.RLock()

	@staticmethod
	def getMD5(info):
		if type(info) == type('s'):
			info = info.decode('utf-8')
		key = md5.new(info.encode('utf-8'))
		return key.digest()

	@staticmethod
	def replaceSpecialCharacters(string, replaceCharacter = ''):

		colon = '%c'%58
		forwardSlash = '%c'%47
		backSlash = '%c'%92
		asterisk = '%c'%42
		questionMask = '%c'%63
		doubleQuote = '%c'%34
		greaterThanSign = '%c'%62
		lessThanSign = '%c'%60
		shugang = '%c'%124

		charSet = [colon, forwardSlash, backSlash, asterisk, questionMask, doubleQuote, greaterThanSign, lessThanSign, shugang]
		for i in charSet:
			string = string.replace(i,replaceCharacter)
		return string
	@staticmethod
	def getSotedListFromDic(dic, reverse = False):
		return sorted(dic.items(), key = lambda dic: dic[1][0:6])

class Log():
	logFilePath = None
	errorlogFilePath = None
	@staticmethod
	def setLogPath(logFilePath, errorlogFilePath):
		Log.logFilePath = logFilePath
		Log.errorlogFilePath = errorlogFilePath

	@staticmethod
	def printAndLog(msg, error = False):
		if type(msg) == type('s'):
			msg = msg.decode('utf-8')
		print msg
		Tools.mylock.acquire()
		if not error:
			logFile = codecs.open(Log.logFilePath, 'a+', 'utf')
			logFile.write(msg)
			logFile.close()
		else:
			errorlogFile = codecs.open(Log.errorlogFilePath, 'a+', 'utf')
			errorlogFile.write(msg)
			errorlogFile.close()
		Tools.mylock.release()

if __name__ == '__main__':
#     myConfig = {}
#     myConfig['basePath'] = 'E:\\MySpace\\Crawel\\Alibuybuy'
#     myConfig['logFilePath'] = 'log.txt'
#     myConfig['errorlogFilePath'] = 'errorlog.txt'
#     Tools.setConfig(myConfig)
#     for i in range(100):
#         if i % 2 == 0:
#             msg = str(i) + ' is a even number.\n'
#             Tools.printAndLog(msg, error = False)
#         else:
#             msg = str(i) + ' is a odd number.\n'
#             Tools.printAndLog(msg, error = True)
	print Tools.replaceSpecialCharacters('000009_【WISE Talk-世界在发生什么】李天放：从硅谷到中国，创业者的心态正在改变.html000004_润物细无声：伟大的品牌化于无形.htmlsdfsd/dfs、：了解啊地方:]\[?')
	print Tools.getMD5('lizhibo')
	print str(Tools.getMD5('lizhibod中国'))
	Log.setLogPath('logpath.txt', 'errorlogpath.txt')
	s = 'mynamie中国中国中国'
	s = u'sdfsdf中国中国中国'
	# print type(s)
	# if type('s') == type(s):
	# 	s = (s.decode('utf-8'))
	# 	print 'haha'
	# print type(s)
	# print type('s')
	Log.printAndLog(s)
