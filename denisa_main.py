import scrapy
from scrapy.crawler import CrawlerProcess
from ourscraper.ourscraper.spiders.analyzerSpiderd import *
from denisa_messages_agents import *
import time

import bs4
from google import google



process = CrawlerProcess()

city="milan"

a = PbSolAgent("agent", "secret",city)
b = AnalyseSourcesAgent("anlizeagent", "secret",process)
c= FindSourcesAgent("fagent","secret","ooo")
a.start()
c.start()
b.start()

time.sleep(5)
print "\n\n Activities in ",city
a.afiseazaActivitati()

file = open('URLs.txt','w') 
response = GoogleSearch().search("atractii turistice")
for result in response.results:
    url_list.append(result.url)
    file.write("\n"+result.url) 
file.close() 


print"***************************FINISH*************************************"
