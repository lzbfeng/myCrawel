# -*- coding: utf-8 -*-
import urllib2

def getResponse(url, userAgent = True):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'             
    headers = { 'User-Agent' : user_agent,
               'Referer' : 'http://www.williamlong.infoq/'}
    if userAgent:
        return urllib2.Request(url, headers = headers)
    else:
        return urllib2.Request(url)