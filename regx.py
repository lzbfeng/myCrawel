# -*- coding: utf-8 -*-
import re
def isNavigationPage(url):
	reg = r'.*(usr|links|about)'
	if re.match(reg, url):
		return False
	return True

urls = ['sdfusrsllfj', 'sdflinkss', 'aaboutsds']

for url in urls:
	print not isNavigationPage(url)


#一个简单的re实例，匹配字符串中的hello字符串


# 将正则表达式编译成Pattern对象，注意hello前面的r的意思是“原生字符串”
pattern = re.compile(r'.*hello')

# 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
match1 = pattern.match('hhello world!')
match2 = pattern.match('helloo world!')
match3 = pattern.match('helllo world!')

#如果match1匹配成功
if match1:
    # 使用Match获得分组信息
    print match1.group()
else:
    print 'match1匹配失败！'


#如果match2匹配成功
if match2:
    # 使用Match获得分组信息
    print match2.group()
else:
    print 'match2匹配失败！'


#如果match3匹配成功
if match3:
    # 使用Match获得分组信息
    print match3.group()
elif match3 == None:
    print 'match3匹配失败！'

url = u'http://news.csdn.net/news/2'
# contains = u'^https?://(www|news|cloud|mobile|sd|programmer|)\.csdn\.net/?.*(mobile|android|ios|移动游戏|html5|游戏引擎|智能硬件)?'
contains = u'^https?://(www|news|cloud|mobile|sd|programmer|)\.csdn\.net/?.*'
contains = u'^https?://((www|news|cloud|mobile|sd|programmer)\.csdn\.net/?.*|blog\.csdn\.net/($|(mobile|web|enterprise|code|www|database|system|cloud|software|other|)/index.html($|\?&?page=\d+)))'
url = u'http://blog.csdn.net/web/index.html?page=2'
notcontains = u'.*(/tag/|download)'
flt = u'^https?://(www\.csdn\.net/article/2.*|blog\.csdn\.net/.*/article/.*)'
# if re.match(contains, url):
# 	print 'successful!!!!!!!!!!!!!!!!aaa'
# else:
# 	print 'aaaaaaaaaaaaaaaaaaaaaaaaaa'

if re.match(contains, url) and re.match(notcontains, url) == None:
	print 'successful!!!!!!!!!!!!!!!!aaa'
else:
	print 'aaaaaaaaaaaaaaaaaaaaaaaaaa'

contains = u'(news|cloud|mobile|sd|programmer)'
notcontains = u'(http|csdn|net|html)'
url = u'news'
# print re.match(u's', u'fdf')
if re.match(notcontains, url) == None:
	print 'successful!!!!!!!!!!!!!!!!bbb'
else:
	print 'aaaaaaaaaaaaaaaaaaaaaaaaaa'

# list = [1,2,3,4]
# print len(list)
# list.extend([])
# print len(list)
#
# url = u'http://www.csdn.net/article/t'
# url = u'http://blog.csdn.net//article/'
# flt = u'^https?://(www\.csdn\.net/article/2.*|blog\.csdn\.net/.*/article/.*)'
# if re.match(flt, url):
# 	print 'successful!!!!!!!!!!!!!!!!'
# else:
# 	print 'aaaaaaaaaaaaaaaaaaaaaaaaaa'


contains = u'^https?://www\.xinli001\.com/(daka/(\?p=\d+|\d+/)?$|info/([A-Za-z]+/|[A-Za-z]+/p\d+/)?)?$'
# contains = u'^https?://((www|news|cloud|mobile|sd|programmer)\.csdn\.net/?.*|blog\.csdn\.net/($|(mobile|web|enterprise|code|www|database|system|cloud|software|other|)/index.html($|\?&?page=\d+)))'
notcontains = u'.*(/tag/|download)'

url = u'http://blog.csdn.net/web/index.html?page=2'
url = u'http://www.xinli001.com/info/'
url = u'http://www.xinli001.com/info/society/p2/'
url = u'http://www.xinli001.com/daka/788/'
url = u'http://www.xinli001.com/daka/?p=2'

if re.match(contains, url) and re.match(notcontains, url) == None:
	print 'successful!!!!!!!!!!!!!!!!ccc'
else:
	print 'aaaaaaaaaaaaaaaaaaaaaaaaaa'

documents = u'^https?://www\.xinli001\.com/(daka/\d+/study/|info/\d+/)$'
url = u'http://www.xinli001.com/info/14657/'
url = u'http://www.xinli001.com/daka/788/study/'
if re.match(documents, url):
	print 'successful!!!!!!!!!!!!!!!!ddd'
else:
	print 'aaaaaaaaaaaaaaaaaaaaaaaaaa'

# categories = u'http://www.xinli001.com/info/$$$/p5/|http://www.xinli001.com/$$$/?p=2'
# categoryOffest = {}
# urls = [u'http://www.xinli001.com/info/news/p5/', u'http://www.xinli001.com/daka/?p=2']
# for cate in [i.strip() for i in categories.split('|')]:
# 	categoryOffest[cate] = cate.find('$$$')
#
# for url in urls:
# 	for i in categoryOffest.items():
# 		if i[0][:i[1]] == url[:i[1]]:
# 			print url
#
# def categoryFilter(self):
# 	contains = u'(news|cloud|mobile|sd|programmer)'
# 	notcontains = u'(http|www|xinli001|com|html||rollingnews)'
# 	return contains, notcontains
#
# contains, notcontains = categoryFilter()
#
# paths = {}
# for url in urls:
# 	fatherurl = url
# 	for j in [i.strip() for i in fatherurl.split('/')]:
# 		getpathflag = 0
# 		for jj in [ii.strip() for ii in j.split('.')]:
# 			url = jj
# 			if re.match(notcontains, url) == None:
# 				if not paths.has_key(jj):
# 					paths[jj] = 1
# 				else:
# 					paths[jj] += 1
# 				path = jj
# 				getpathflag = 1
# 				break
# 		if getpathflag == 1:
# 			break

urls = [u'http://www.xinli001.com/info/news/p5/', u'http://www.xinli001.com/daka/?p=2']
url = u'http://www.xinli001.com/info/news/p5/'
url = u'http://www.xinli001.com/daka/?p=2'
myItems = re.findall(u'http://www.xinli001.com/info/(.*?)/', url, re.S)
# myItems = re.findall(u'http://www.xinli001.com/(.*?)/', url, re.S)
items = []
print myItems
print len(myItems)
for item in myItems:
	print item

print 'exit'
	# items.append([item[0].replace("\n","")])

