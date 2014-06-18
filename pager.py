import re
from threading import Timer
from BeautifulSoup import BeautifulSoup as BS
from myUtils import *
from myUrllib import *
from config import GLOBAL

class PageType:
	navi = 0
	docu = 1
	other = 2

class URLInfo:

	def __init__(self, url, fatherurl, title, type, otherinfo=None):
		self.url = url
		self.fatherurl = fatherurl
		self.title = title
		self.otherinfo = otherinfo
		self.type = type

class Pager():

	def __init__(self, url, config):
		self.url = url
		self.config = config
		self.isNavi = self._isNavigation(url)
		self.isDoc = self._isDocument(url)
		self.timeout = config[u'timeout']

	def _isNavigation(self, url):
		contains = self.config['naviContains']
		notcontains = self.config['naviNotContains']
		if ((re.match(contains, url)) and (re.match(notcontains, url) == None)):
			return True
		return False

	def _isDocument(self, url):
		contains = self.config['document']
		if re.match(contains, url):
			return True
		return False

	def getURL(self):
		return self.url

	def isNavigation(self):
		return self.isNavi

	def isDocument(self):
		return self.isDoc

	def reconstractOneURL(self, url):
		if u'javascript' not in url:
			if 'http://' not in url and 'https://' not in url:
				if len(url) != 0 and '/' == url[0]:
					url = self.getPageDomain()[:-1] + url
				else:
					url = self.getPageDomain() + url
			return url
		else:
			return None

	def getPageURLsInfo(self, pagesoup):
		return self.processPage(pagesoup)

	def getOneURLInfo(self, url, taga):
		return self.processURL(url, taga)

	# overwrite
	def processURL(self, url, taga):
		url = self.reconstractOneURL(url)
		if url != None:
			if self._isDocument(url):
				title = ''
				if len(taga.contents) > 0:
					if taga.img != None and len(taga.img.attrs) >= 5:
						title = taga.img['alt']
					else:
						title = taga.contents[0]
				return URLInfo(url, self.url, title, PageType.docu)
			elif self._isNavigation(url):
				return URLInfo(url, self.url, None, PageType.navi)
			else:
				return None
		return None

	# overwrite
	def processPage(self, pagesoup):
		urls = []
		for taga in pagesoup.findAll('a'):
			s = str(taga).decode('utf-8')
			if u'href' in s:
				try:
					url = taga[u'href']
					urlInfo = self.getOneURLInfo(url, taga)
					if urlInfo != None:		#if this url is not a navi or docu url, then will get a None
						urls.append([urlInfo.url, urlInfo.fatherurl, urlInfo.title])
				except Exception, e:
					Log.printAndLog('there is an error occured in function getPageURLsInfo and it is: ' + str(e))
		return urls

	def getPageURLs(self):
		if self.isNavi:		# this must be a navigation page.
			pagesoup = self._getAPageSoup()
			return self.getPageURLsInfo(pagesoup)
		else:
			return []

	def _getAPageSoup(self):
		req = getResponse(self.url)
		page = urllib2.urlopen(req, timeout=20)
		soup = BS(page)
		return soup
	def getURLMainframe(self, url):
		try:
			url = url.split('/')[2]
			domain = url.split('.')[1]
			return domain
		except Exception, e:
			Log.printAndLog('there is an error occured, and it is: ' + str(e) + ', and the url is: ' + url + '\n', True)
			return None
	def getPageDomain(self):
		temps = self.url.split('/')
		return temps[0] + '/' + temps[1] + '/' + temps[2] + '/'


class AnotherPager(Pager):

	def __init__(self, url, config):
		Pager.__init__(self, url, config)

	# overwrite
	def processPage(self, pagesoup):
		urls = []
		for taga in pagesoup.findAll('a'):
			s = str(taga).decode('utf-8')
			if u'href' in s:
				try:
					url = taga[u'href']
					urlInfo = self.getOneURLInfo(url, taga)
					if urlInfo != None:		#if this url is not a navi or docu url, then will get a None
						urls.append([urlInfo.url, urlInfo.fatherurl, urlInfo.title])
				except Exception, e:
					Log.printAndLog('there is an error occured in function getPageURLsInfo and it is: ' + str(e))
		return urls

	# overwrite
	def processURL(self, url, taga):
		url = self.reconstractOneURL(url)
		if url != None:
			if self._isDocument(url):
				title = ''
				if len(taga.contents) > 0:
					if taga.img != None and len(taga.img.attrs) >= 5:
						title = taga.img['alt']
					else:
						title = taga.contents[0]
				if u'daka' in url and taga.img != None:
					url += u'study/'
					return None
				return URLInfo(url, self.url, title, PageType.docu)
			elif self._isNavigation(url):
				return URLInfo(url, self.url, None, PageType.navi)
			else:
				return None
		return None


def generateOnePager(url, config):
	return AnotherPager(url, config)