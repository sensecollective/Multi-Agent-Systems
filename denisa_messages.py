import spade


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
        sb.defineMessage("Ce faci?")
        rb = self.ReceiveBehav()
        self.setDefaultBehaviour(sb)

        cooking_template = spade.Behaviour.ACLTemplate()
        cooking_template.setOntology("cooking")
        mt = spade.Behaviour.MessageTemplate(cooking_template)

        self.addBehaviour(rb, mt)


#-------------------------------------------------------------------------------------------PbSolAgent---------------------------------------------------------------------


class PbSolAgent(GeneralAgent):
    
    problem=""
    
    def __init__ (self,identificator,parola,problem):
            
        GeneralAgent.__init__(self,identificator,parola)
        self.problem=problem
        
        print "I am ",self.identificator,"and i have id=",self.name,"and pass= ",self.password,"and pb=",self.problem
            

    def _setup(self):
        print "MyAgent starting . . ."
        sb = self.SendBehav()
        sb.defineMessage("MEsaj de la PbSolAgent")
        sb.defineReceiver("anlizeagent")
        rb = self.ReceiveBehav()
        self.setDefaultBehaviour(sb)

        cooking_template = spade.Behaviour.ACLTemplate()
        cooking_template.setOntology("cooking")
        mt = spade.Behaviour.MessageTemplate(cooking_template)

        self.addBehaviour(rb, mt)
        

#-------------------------------------------------------------------------------------------FindSourcesAgent---------------------------------------------------------------------


class FindSourcesAgent(GeneralAgent):
    
    sources=[]
    
    def __init__ (self,identificator,parola,problem):
            
        GeneralAgent.__init__(self,identificator,parola)
        self.problem=problem
        
        print "I am ",self.identificator,"and i have id=",self.name,"and pass= ",self.password,"and pb=",self.problem
            

    def _setup(self):
        print "MyAgent starting . . ."
        sb = self.SendBehav()
        sb.defineMessage("MEsaj de la Analyser")
        sb.defineReceiver("fagent")
        rb = self.ReceiveBehav()
        self.setDefaultBehaviour(sb)

        cooking_template = spade.Behaviour.ACLTemplate()
        cooking_template.setOntology("cooking")
        mt = spade.Behaviour.MessageTemplate(cooking_template)

        self.addBehaviour(rb, mt)
        
        
    
    
    

#-------------------------------------------------------------------------------------------AnalyseSourcesAgent---------------------------------------------------------------------


class AnalyseSourcesAgent(GeneralAgent):
    
    results=[]
    
    def __init__ (self,identificator,parola,problem):
            
        GeneralAgent.__init__(self,identificator,parola)
        self.problem=problem
        
        print "I am ",self.identificator,"and i have id=",self.name,"and pass= ",self.password,"and pb=",self.problem
            

    def _setup(self):
        print "MyAgent starting . . ."
        sb = self.SendBehav()
        sb.defineMessage("Mesaj de la Fider")
        sb.defineReceiver("agent")
        rb = self.ReceiveBehav()
        self.setDefaultBehaviour(sb)

        cooking_template = spade.Behaviour.ACLTemplate()
        cooking_template.setOntology("cooking")
        mt = spade.Behaviour.MessageTemplate(cooking_template)

        self.addBehaviour(rb, mt)
        
        
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    a = PbSolAgent("agent", "secret","pb1")
    b = AnalyseSourcesAgent("anlizeagent", "secret","pb2")
    c= FindSourcesAgent("fagent","secret","ooo")
    a.start()
    b.start()
    c.start()
