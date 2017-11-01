import scrapy
from scrapy.crawler import CrawlerProcess
from ourscraper.ourscraper.spiders.analyzerSpiderd import *

import spade

import csv
import re

import bs4
from ag.googlesearch.googlesearch.googlesearch import *
from google import google

import time

server_IP="127.0.0.1"


#-------------------------------------------------------------------------------------------GeneralAgent---------------------------------------------------------------------
class GeneralAgent(spade.Agent.Agent):
    
    name=""
    identificator=""
    password=""
    
    
    def __init__ (self,identificator,parola):
        self.identificator=identificator
        self.name=identificator+"@"+server_IP
        self.password=parola
            
        print "I am ",self.identificator,"and i have id=",self.name,"and pass= ",self.password
        spade.Agent.Agent.__init__(self,self.name,self.password)
        
            
#---------------------------------------------------SendBehaviour----------------------------------------
            
    class SendBehav(spade.Behaviour.OneShotBehaviour):
        
        message=""
        receiver=""
        
        def defineMessage(self,message):
            self.message=message
        
        def defineReceiver(self,receiver):
            self.receiver=receiver
            
        def _process(self):
            # First, form the receiver AID
            # the receiver agent
            receiver = spade.AID.aid(name=self.receiver+"@"+server_IP,
                                     addresses=["xmpp://"+self.receiver+"@"+server_IP]) 

            # Second, build the message
            self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
            self.msg.setPerformative("inform")  # Set the "inform" FIPA performative
            self.msg.setOntology("cooking")  # Set the ontology of the message content
            self.msg.setLanguage("OWL-S")  # Set the language of the message content
            self.msg.addReceiver(receiver)  # Add the message receiver
            self.msg.setContent(self.message)  # Set the message content
            # print self.msg
            # Third, send the message with the "send" method of the agent
            self.myAgent.send(self.msg)

#---------------------------------------------------ReceiveBehaviour--------------------------------------
    class ReceiveBehav(spade.Behaviour.Behaviour):
        """This behaviour will receive all kind of messages"""
                
        def _process(self):
            self.msg = None

            # Blocking receive for 10 seconds
            self.msg = self._receive(True, 10)

            # Check wether the message arrived
            if self.msg:
                print "I got a message !"
                print self.msg.content
            else:
                print "I waited but got no message"
                




    def _setup(self):
        print "MyAgent starting . . ."
        sb = self.SendBehav()
        sb.defineMessage("Hello")
        rb = self.ReceiveBehav()
        self.setDefaultBehaviour(sb)

        cooking_template = spade.Behaviour.ACLTemplate()
        cooking_template.setOntology("cooking")
        mt = spade.Behaviour.MessageTemplate(cooking_template)

        self.addBehaviour(rb, mt)


#-------------------------------------------------------------------------------------------PbSolAgent---------------------------------------------------------------------


class PbSolAgent(GeneralAgent):
    
    problem=""
    url=""
    
    def __init__ (self,identificator,parola,problem):
            
        GeneralAgent.__init__(self,identificator,parola)
        self.problem=problem
        self.url='http://www.touropia.com/tourist-attractions-in-'+problem+'/'
        
        print "I am ",self.identificator,"and i have id=",self.name,"and pass= ",self.password,"and pb=",self.problem
            
    def afiseazaActivitati(self):
        with open('analyzerResults.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            print "\n---------------------------------------------------"
            for row in reader:
                r=row['ranking']
                # r=re.sub('[.\xc2\xa0]','',r)
                t=row['title']
                # t = re.sub('[!@#$(]', '', t)
                
                print '******' +r +'  ' +t 
            print "---------------------------------------------------\n"
            
    def showURLs(self):
        print "\n--------------------URLs: ---------------------------"
        file = open('URLs.txt', 'r') 
        for line in file: 
            print "\n "+line
        print "---------------------------------------------------\n"
        
    def _setup(self):
        print "MyAgent starting . . ."
        sb = self.SendBehav()
        sb.defineMessage(self.problem)
        sb.defineReceiver("fagent")
        self.setDefaultBehaviour(sb)
        
        rb = self.ReceiveBehav()
        cooking_template = spade.Behaviour.ACLTemplate()
        cooking_template.setOntology("cooking")
        mt = spade.Behaviour.MessageTemplate(cooking_template)
        self.addBehaviour(rb, mt)
        
        
        
        sb2 = self.SendBehav()
        sb2.defineMessage(self.url)
        sb2.defineReceiver("anlizeagent")
        self.addBehaviour(sb2)
        
        
    

#-------------------------------------------------------------------------------------------FindSourcesAgent---------------------------------------------------------------------


class FindSourcesAgent(GeneralAgent):
    
    sources=[]
    
    def __init__ (self,identificator,parola):
            
        GeneralAgent.__init__(self,identificator,parola)
        
        print "I am ",self.identificator,"and i have id=",self.name,"and pass= ",self.password
    
     #---------------------------------------------------ReceiveBehaviour--------------------------------------
    class ReceiveBehavFinder(spade.Behaviour.Behaviour):
        
        city=""
        isCityReceived=False
        
        def __init__ (self):
            spade.Behaviour.Behaviour.__init__(self)
                
        def _process(self):
            self.msg = None
            
            # Blocking receive for 10 seconds
            self.msg = self._receive(True, 10)

            # Check wether the message arrived
            if self.msg:
                print "Finder agent: I got a message !I received the city and now I will search for URLs..."
                #search on google using the city receives through the message received from the PobSolAgent
                self.city=self.msg.content
                isCityReceived=True
                
                url_list=[]
                file = open('URLs.txt','w') 
                text="touristic objectives "+self.city
                response = GoogleSearch().search(text)
                for result in response.results:
                    url_list.append(result.url)
                    file.write("\n"+result.url) 
            else:
                print "Finder agent: I waited but got no message"   
                
        # def getCity(self):
        #     while(isCityReceived==False):
        #         print "a"
        #     return self.city
            
    def _setup(self):
        print "MyAgent starting . . ."
        
        rb = self.ReceiveBehavFinder()
        cooking_template = spade.Behaviour.ACLTemplate()
        cooking_template.setOntology("cooking")
        mt = spade.Behaviour.MessageTemplate(cooking_template)
        self.addBehaviour(rb, mt)
        
        # desiredCity=rb.getCity()
        
        # print "********************88-------------------------------------:  ",desiredCity
        
        
        # url_list=[]
        # file = open('URLs.txt','w') 
        # text="touristic objectives "+desiredCity
        # response = GoogleSearch().search(text)
        # for result in response.results:
        #     url_list.append(result.url)
        #     file.write("\n"+result.url) 
        # file.close() 
        
        
        sb = self.SendBehav()
        # mes="\n Message from Finder: "
        # for u in url_list:
        #     mes+="\n"
        #     mes+=u
        sb.defineMessage("Message from Finder")
        sb.defineReceiver("agent")
        self.setDefaultBehaviour(sb)
    
    

#-------------------------------------------------------------------------------------------AnalyseSourcesAgent---------------------------------------------------------------------

spiderAnalyser=AnalyzerspiderSpiderd()

class AnalyseSourcesAgent(GeneralAgent):
    
    results=[]
    city=""
    process = ""
    
    def proba(self,text):
        print text
        
        
    def __init__ (self,identificator,parola,process):
            
        GeneralAgent.__init__(self,identificator,parola)
        self.process=process
        
        print "I am ",self.identificator,"and i have id=",self.name,"and pass= ",self.password
            
    #---------------------------------------------------ReceiveBehaviour--------------------------------------
    class ReceiveBehavAnalyser(spade.Behaviour.Behaviour):
        process=""
        
        
        
        def __init__ (self,process):
            spade.Behaviour.Behaviour.__init__(self)
            self.process=process
                
        def _process(self):
            self.msg = None

            
            # Blocking receive for 10 seconds
            self.msg = self._receive(True, 10)

            # Check wether the message arrived
            if self.msg:
                print "Analyse agent: I got a message !I received the city and now I will search for activities..."
                #set the city for the spider with the message received from the PobSolAgent
                spiderAnalyser.setURL(self.msg.content) 
                
                
                self.process.crawl(spiderAnalyser)
                self.process.start()
                
                print "Analyse agent: I did the research"
                
                
                
            else:
                print "I waited but got no message"
                
        
    def _setup(self):
        print "MyAgent starting . . ."
        
        sb = self.SendBehav()
        sb.defineMessage("Message from Analyzer \n \n")
        sb.defineReceiver("agent")
        self.setDefaultBehaviour(sb)
        
        rb = self.ReceiveBehavAnalyser(self.process)
        cooking_template = spade.Behaviour.ACLTemplate()
        cooking_template.setOntology("cooking")
        mt = spade.Behaviour.MessageTemplate(cooking_template)
        self.addBehaviour(rb, mt)
        
        
        
      
    
    
    
    
# if __name__ == "__main__":
#     a = PbSolAgent("agent", "secret","pb1")
#     b = AnalyseSourcesAgent("anlizeagent", "secret","pb2")
#     c= FindSourcesAgent("fagent","secret","ooo")
#     a.start()
#     b.start()
#     c.start()
