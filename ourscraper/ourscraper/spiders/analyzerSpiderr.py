# -*- coding: utf-8 -*-
import scrapy


class AnalyzerspiderrSpider(scrapy.Spider):
    name = 'analyzerSpiderr'
    allowed_domains = ['http://www.themost10.com/tourist-attractions-in-rome/']
    start_urls = ['http://www.themost10.com/tourist-attractions-in-rome/']

    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'analyzerr.csv'
   }
   
    def parse(self, response):
        titles = response.css("h2::text").extract()
       
        #Give the extracted content row wise
        for item in zip(titles):
            #create a dictionary to store the scraped info
            scraped_info = {
                'title' : item[0]
            }

            #yield or give the scraped info to scrapy
            yield scraped_info