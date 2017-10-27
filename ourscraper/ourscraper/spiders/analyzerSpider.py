# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess


class AnalyzerspiderSpider(scrapy.Spider):
    
    name = 'analyzerSpider'
    city="milan"
    url='http://www.touropia.com/tourist-attractions-in-'+city+'/'
    allowed_domains = [url]
    start_urls = [url]
    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'analyzer.csv'
   }
    
    
   
    def parse(self, response):
        titles = response.css(".toptitle::text").extract()
        rankings = response.css('.topnumber::text').extract()
       
        #Give the extracted content row wise
        for item in zip(titles,rankings):
            #create a dictionary to store the scraped info
            scraped_info = {
                'title' : item[0],
                'ranking' : item[1]
            }

            #yield or give the scraped info to scrapy
            yield scraped_info
            
spider=AnalyzerspiderSpider()
process = CrawlerProcess()
process.crawl(spider)
process.start()