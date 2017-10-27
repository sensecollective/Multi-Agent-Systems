import scrapy
from scrapy.crawler import CrawlerProcess
from ourscraper.ourscraper.spiders.analyzerSpiderd import *
from denisa_messages_agents import *
import time

process = CrawlerProcess()

city="milan"

a = PbSolAgent("agent", "secret",city)
b = AnalyseSourcesAgent("anlizeagent", "secret",process)
c= FindSourcesAgent("fagent","secret")
a.start()
c.start()
b.start()


time.sleep(5)
print "\n\n Activities in ",city
a.afiseazaActivitati()

# time.sleep(5)
# print "\n\n URLs for ",city
# a.showURLs()

