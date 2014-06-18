from BeautifulSoup import BeautifulSoup as BS

pagesoup = BS(open(u'/home/hadoop/crawelData/12.html'))

for i in pagesoup.findAll(u'a'):
	# print i
	if i.img != None:
		if i[u'href'] == u'http://www.xinli001.com/site/':
			print
		print i.img
		s = i.img
		if len(s.attrs) >= 5:
			print s[u'alt']