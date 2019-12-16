# -*- coding: utf-8 -*-
import scrapy
import re
# from scrapy.http.response.text import TextResponse
# from scrapy.http.response import Response
from scrapy.selector.unified import Selector


g_lstBadChar = ['\\', '*', ':' , '\"', '?', '>','<', '|']
g_szOkChar = '_'
g_szExtension = '.html'
#g_szKeyWord = 'Auto Probe'
# g_szPattern = 'probe'
g_szPattern = 'Third Person Controller'


class CgsosoSpider(scrapy.Spider):
    name = 'cgsoso'
    allowed_domains = ['cgsoso.com']
    start_urls = ['http://www.cgsoso.com/forum.php?mod=forumdisplay&fid=211&filter=sortall&sortall=1']
    theLoginPost = 'http://www.cgsoso.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LkJS0&inajax=1'
    theUserName = 'outaooutao@126.com'
    thePassWord = 'e10adc3949ba59abbe56e057f20f883e'

    def start_requests(self):
        yield scrapy.FormRequest(
            url=CgsosoSpider.theLoginPost,
            formdata={'username': CgsosoSpider.theUserName, 'password': CgsosoSpider.thePassWord},
            callback=self.after_login)

    @staticmethod
    def save_web_page(response):
        if response.url[-1] == '/':
            fileName = response.url.split('/')[-2]
        else:
            fileName = response.url.split('/')[-1]
        for szBadChar in g_lstBadChar:
            fileName = fileName.replace(szBadChar, g_szOkChar)
        fileName = "output/{0}{1}"%(fileName, g_szExtension)
        open(fileName, 'wb+').write(response.body)

    def parse(self, response):
        lstLinks = response.selector.xpath('//a')
        for link in lstLinks:
            szLinkText = link.xpath('text()').get()
            if szLinkText is not None and re.search(g_szPattern, szLinkText, re.I) is not None:
                szHref = link.xpath('@href').get()
                yield scrapy.Request(szHref, callback=CgsosoSpider.save_web_page)

        # pages
        # lstNewPages = response.selector.xpath('//div[@class="pg"]/a/@href').getall()
        # for szNewPages in lstNewPages:
        #     yield scrapy.Request(szNewPages,dont_filter=True)
        # just next page

        # szNext = response.selector.xpath('//span[@id="fd_page_bottom"]/div[@class="pg"]/a[@class="nxt"]/@href'
        #                                  ).get()
        # if szNext is not None:
        #     yield scrapy.Request(szNext, dont_filter=True)

    def after_login(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)


