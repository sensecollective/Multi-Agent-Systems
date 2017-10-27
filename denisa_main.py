import scrapy
from scrapy.crawler import CrawlerProcess
from ourscraper.ourscraper.spiders.analyzerSpiderd import *
from denisa_messages_agents import *
import time


process = CrawlerProcess()

city="milan"

a = PbSolAgent("agent", "secret",city)
b = AnalyseSourcesAgent("anlizeagent", "secret",process)
#c= FindSourcesAgent("fagent","secret","ooo")
a.start()
b.start()
#c.start()

time.sleep(3)
print "\n\n Activities in ",city
a.afiseazaActivitati()



