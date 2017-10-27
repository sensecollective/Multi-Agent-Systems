# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
import io
import re


#---------------------------------------------------------------------------AnalyzerSpider------------------------------------------------------------------------

class AnalyzerspiderSpiderd(scrapy.Spider):
    
    name = 'analyzerSpider'
    city=""
    url=''
    allowed_domains = []
    start_urls = []
    scraped_info=""
    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'analyzerResults.csv'
   }
    
    
    def setCity(self,city):
        print "-----------------------------setcity---------------------"
        self.city=city
        self.url='http://www.touropia.com/tourist-attractions-in-'+city+'/'
        #here should be that URLs found by FinderAgent 
        self.allowed_domains.append(self.url) 
        self.start_urls.append(self.url)
            
        print "I am a spider with name:  ",self.name,"and I am looking for activities in city=",self.city
      
   
    def parse(self, response):
        titles = response.css(".toptitle::text").extract()
        rankings = response.css('.topnumber::text').extract()

        #Give the extracted content row wise
        for item in zip(titles,rankings):
            #create a dictionary to store the scraped info
            r=item[0]
            r=re.sub('[.\xc2\xa0]','',r)
            t=item[1]
            t = re.sub('[()]', '', t)
            scraped_info = {
                'title' : r,
                'ranking' : t
            }
           
           
            #yield or give the scraped info to scrapy
            yield scraped_info
 

# spider=AnalyzerspiderSpiderd()
# spider.setCity('milan')
# process = CrawlerProcess()
# process.crawl(spider)
# process.start()