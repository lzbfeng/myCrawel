class page:

	def __init__(self, url, fatherurl, title):
		self.url = url
		self.fatherurl = fatherurl
		self.title = title

	def overwrite(self):
		print self.url

class pageer(page):

	def __init__(self, url, fatherurl, title):
		page.__init__(self, url, fatherurl, title)

	def overwrite(self):
		print self.title


p = pageer('lll', 'zzz', 'tttt')

p.overwrite()

from pager import *

